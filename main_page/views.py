from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import SocialMedia, MainPage, MainPageVideo, Analysis
from .serializers import MainPageSerializer, AnalysisSerializer, AnalysisDetailSerializer


class MainPageAPIView(GenericAPIView):
    serializer_class = MainPageSerializer

    def get_main_page_videos(self):
        try:
            return MainPageVideo.objects.all()
        except:
            return None

    def get_social_media(self):
        try:
            return SocialMedia.objects.all()
        except:
            return None

    def get_main_page(self):
        try:
            return MainPage.objects.all()[0]
        except:
            return None

    def get(self, request):
        videos = self.get_main_page_videos()
        social_media = self.get_social_media()
        main_page = self.get_main_page()
        data = {
            'videos': videos,
            'social_medias': social_media,
            'img': main_page.img,
            'first_btn': main_page.first_btn,
            'second_btn': main_page.second_btn,
            'third_btn': main_page.third_btn,
            'first_btn_lat': main_page.first_btn_lat,
            'second_btn_lat': main_page.second_btn_lat,
            'third_btn_lat': main_page.third_btn_lat,
            'link': main_page.link
        }
        serializer = MainPageSerializer(data)
        return Response(serializer.data)


class AnalysisListAPIView(ListAPIView):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

    @swagger_auto_schema(
        responses={
            200: AnalysisSerializer,
            400: ''
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AnalysisAPIView(RetrieveAPIView):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisDetailSerializer

    @swagger_auto_schema(
        responses={
            200: AnalysisDetailSerializer,
            400: ''
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)