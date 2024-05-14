from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, get_user_model, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

from client.models import ClientDevice
from user.authentication import TokenAuthentication
from .serializers import LogOutSerializer, UserSerializer, LoginSerializer

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
        

class TokenLogin(APIView):
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
            if not created:
                return Response({"details": "Кечирсиз, сизнинг аккаунтингизга бирдан зиёд телефон орқали кирилган, бу бизнинг иловамизни истифода қилиш келишувига мувофик."}, status=400)
            return Response({**UserSerializer(user).data,'token': token.key}, status=200)
        
        return Response(serializer.errors, status=400)


class TokenLogout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response(status=204)

class TokenMe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


