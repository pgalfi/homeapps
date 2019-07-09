import locale

from django.contrib.auth.models import User
from rest_framework import serializers

from housing.models import Advertiser, HouseProspect, HouseLink, HouseProperty, HouseView


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = ['id', 'name', 'web', 'currency_name']


class HouseLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseLink
        fields = ['id', 'link_type', 'link']


class HousePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseProperty
        fields = ['id', 'name', 'data']


class HouseProspectSerializer(serializers.ModelSerializer):
    links = HouseLinkSerializer(many=True)
    properties = HousePropertySerializer(many=True)
    advertiser_name = serializers.SlugField(source="advertiser.name", read_only=True)
    advertiser_currency = serializers.SlugField(source="advertiser.currency_name", read_only=True)
    price = serializers.CharField(source="price_format", read_only=True)
    post_date = serializers.CharField(source="post_date_format", read_only=True)
    viewed_date = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = HouseProspect
        fields = ['id', 'description', 'description_state',
                  'zip_location', 'price', 'size', 'rooms',
                  'reference_id', 'post_date', 'advertiser',
                  'advertiser_name', 'advertiser_currency',
                  'links', 'properties', 'viewed_date', 'liked']

    def get_viewed_date(self, house):
        vdates = list(house.viewed.filter(pk=self.context["request"].user.id).values("user_to_house__view_date"))
        if len(vdates) > 0:
            locale.setlocale(locale.LC_ALL, house.advertiser.locale_name)
            return vdates[0]["user_to_house__view_date"].strftime("%d %b %Y")
        else: return None

    def get_liked(self, house):
        blikes = house.liked.filter(pk=self.context["request"].user.id)
        if blikes.count() > 1: return True
        return False


