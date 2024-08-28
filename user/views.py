import datetime

import pytz
from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, get_user_model, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group

from client.models import ClientDevice
from medical_inventory import settings
from user.authentication import TokenAuthentication
from .models import SubscriptionType, Subscription
from .serializers import LogOutSerializer, UserSerializer, LoginSerializer, SubscriptionSerializer, \
    SubscriptionTypeSerializer

User = get_user_model()

class SignUpView(CreateAPIView):
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SignInView(APIView):
    authentication_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            device_id = request.data.get('device_id')
            if device_id is None:
                return Response({'message': 'device_id field is required'}, status=400)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                ClientDevice.get_or_create_device(user=user, device_id=device_id)
                return Response(UserSerializer(user).data)
            else:
                return Response({'message': 'Invalid credentials.'}, status=401)

        return Response(serializer.errors, status=400)
    
    
class SignOutView(APIView):
    authentication_classes = []
    def post(self, request):
        serializer = LogOutSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        device = ClientDevice.get_active_device(serializer.validated_data['device_id'])
        device.is_active = False
        device.save()
        return Response({'message': 'Success'}, status=200)
    
    
class MeView(APIView):
    authentication_classes = []
    
    def post(self, request):
        serializer = LogOutSerializer(data=request.data)
        if not serializer.is_valid():
            raise AuthenticationFailed(detail="Device id field not found")
        device = ClientDevice.get_active_device(serializer.validated_data['device_id'])
        data = UserSerializer(device.user).data
        data['paid'] = False
        return Response({**data})
        

class TokenLogin(GenericAPIView):
    queryset = Token.objects.all()
    serializer_class = LoginSerializer
    authentication_classes = []
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if not user:
                return Response({'message': 'Invalid credentials.'}, status=401)
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            request.data['username'] = user
            if not created:
                return Response({"details": "Кечирсиз, сизнинг аккаунтингизга бирдан зиёд телефон орқали кирилган, бу бизнинг иловамизни истифода қилиш келишувига мувофик."}, status=400)
            return Response({**UserSerializer(user).data, 'token': token.key}, status=200)
        
        return Response(serializer.errors, status=400)


class TokenLogout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response(status=204)


class TokenMe(GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

class SubscriptionTypeView(GenericAPIView):
    queryset = SubscriptionType
    serializer_class = SubscriptionTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.request.query_params.get('pk', None)
        try:
            queryset = SubscriptionType.objects.get(pk=pk)
        except:
            raise ValidationError("Invalid input")
        return queryset

    def get(self, request):
        subscriptions = SubscriptionType.objects.all()
        serializer = SubscriptionTypeSerializer(subscriptions, many=True)
        return Response(serializer.data)


class SubscriptionView(GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_subscription_type(self, pk):
        try:
            return SubscriptionType.objects.get(pk=pk)
        except:
            raise Http404

    def get_active_subscription(self, user):
        try:
            return Subscription.objects.get(user=user, is_active=True)
        except:
            return None

    def end_date(self, subscription_type):
        date = datetime.datetime.today()
        if subscription_type.name == "VIP":
            year = 3000
            month = date.month
        else:
            month = date.month + int(subscription_type.period)
            year = date.year
            if month > 12:
                month %= 12
                year += 1
        end_date = datetime.datetime(year=year, month=month,
                                     day=date.day, hour=date.hour,
                                     minute=date.minute, second=date.second,
                                     microsecond=date.microsecond)
        return end_date

    def get(self, request, pk):
        subscription_type = self.get_subscription_type(pk)
        request.data['user'] = request.user.id
        request.data['subscription'] = subscription_type.id
        subscription = self.get_active_subscription(request.user.id)
        if subscription:
            request.data['end_date'] = subscription.end_date
            request.data['is_active'] = subscription.is_active
            serializer = SubscriptionSerializer(subscription, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            request.data['end_date'] = self.end_date(subscription_type)
            serializer = SubscriptionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                group_subscribers = Group.objects.get(name='Subscriber')
                group_subscribers.user_set.add(request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
