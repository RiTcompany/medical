from rest_framework import serializers

from main_page.models import MainPage, SocialMedia, MainPageVideo, Analysis, Indicator


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


class IndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator
        fields = '__all__'


class AnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Analysis
        fields = '__all__'


class AnalysisDetailSerializer(serializers.ModelSerializer):
    indicators = IndicatorSerializer(many=True, allow_null=True)

    class Meta:
        model = Analysis
        fields = '__all__'
