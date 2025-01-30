from rest_framework import serializers

from main_page.models import MainPage, SocialMedia, MainPageVideo


class SocialMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialMedia
        fields = "__all__"


class MainPageVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainPageVideo
        fields = "__all__"


class MainPageSerializer(serializers.ModelSerializer):
    videos = serializers.ListField(child=MainPageVideoSerializer())
    social_medias = serializers.ListField(child=SocialMediaSerializer())

    class Meta:
        model = MainPage
        fields = '__all__'
