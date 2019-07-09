import datetime
import locale
import re
import time

from django.contrib.auth.models import User
from django.db import models

from housing import constants


class Advertiser(models.Model):
    name = models.CharField(max_length=2048)
    web = models.URLField()
    currency_name = models.CharField(max_length=1024)
    locale_name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class HouseProspect(models.Model):
    zip_location = models.CharField(max_length=1024, null=True, default=None)
    description = models.TextField(null=True, default=None)
    description_state = models.IntegerField(choices=constants.CONTENT_STATES)
    price = models.FloatField(null=True, default=None)
    size = models.FloatField(null=True, default=None)
    rooms = models.FloatField(null=True, default=None)
    reference_id = models.CharField(max_length=2048)
    post_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    viewed = models.ManyToManyField(User, through="HouseView", related_name="views")
    liked = models.ManyToManyField(User, related_name="likes")

    @property
    def price_format(self):
        locale.setlocale(locale.LC_ALL, self.advertiser.locale_name)
        return '{0:n}'.format(self.price)

    @property
    def post_date_format(self):
        locale.setlocale(locale.LC_ALL, self.advertiser.locale_name)
        return self.post_date.date().strftime("%d %b %Y")


class HouseLink(models.Model):
    house = models.ForeignKey(HouseProspect, on_delete=models.CASCADE,
                              related_name="links")
    link_type = models.IntegerField(choices=constants.HOUSING_LINK_TYPES)
    link = models.URLField()


class HouseProperty(models.Model):
    house = models.ForeignKey(HouseProspect, on_delete=models.CASCADE,
                              related_name="properties")
    name = models.CharField(max_length=2048)
    data = models.TextField()


class HouseView(models.Model):
    house = models.ForeignKey(HouseProspect, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_to_house")
    view_date = models.DateTimeField(auto_now_add=True)

