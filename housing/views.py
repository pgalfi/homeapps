import locale

from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.response import Response

from housing.models import HouseProspect, Advertiser, HouseView
from housing.serializers import HouseProspectSerializer


def get_start_end(range):
    range = range.strip()
    if len(range) == 0: return (None, None)
    ranges = range.split("-")
    if len(ranges) == 1:
        start = range
        end = range
    elif len(ranges[0]) == 0:
        start = None
        end = ranges[1]
    elif len(ranges[1]) == 0:
        start = ranges[0]
        end = None
    else:
        start = ranges[0]
        end = ranges[1]
    return (start, end)


class HouseProspectFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        advertisers = request.query_params.getlist("advertisers", [])
        zip_filter = request.query_params.get("zip_filter", "").strip()
        start_zip, end_zip = get_start_end(zip_filter)
        price_filter = request.query_params.get("price_filter", "")
        start_price, end_price = get_start_end(price_filter)
        size_filter = request.query_params.get("size_filter", "")
        start_size, end_size = get_start_end(size_filter)
        room_filter = request.query_params.get("room_filter", "")
        start_rooms, end_rooms = get_start_end(room_filter)
        desc_text = request.query_params.get("desc_text", None)
        # show_viewed = request.query_params.get("show_viewed", None)
        # if show_viewed is not None: show_viewed = True
        # show_liked = request.query_params.get("show_liked", None)
        # if show_liked is not None: show_liked = True

        queryset = queryset.filter(is_available=True)
        if len(advertisers) > 0:
            queryset = queryset.filter(advertiser_id__in=advertisers)
        if start_rooms is not None:
            queryset = queryset.filter(rooms__gte=start_rooms)
        if end_rooms is not None:
            queryset = queryset.filter(rooms__lte=end_rooms)
        if start_size is not None:
            queryset = queryset.filter(size__gte=start_size)
        if end_size is not None:
            queryset = queryset.filter(size__lte=end_size)
        if start_price is not None:
            queryset = queryset.filter(price__gte=start_price)
        if end_price is not None:
            queryset = queryset.filter(price__lte=end_price)
        if desc_text is not None and len(desc_text.strip()) > 0:
            queryset = queryset.filter(description__icontains=desc_text)
        if start_zip is not None:
            queryset = queryset.filter(zip_location__gte=start_zip)
        if end_zip is not None:
            queryset = queryset.filter(zip_location__lte=end_zip)
        # if show_viewed is None:
        #     queryset = queryset.filter(Q(views__user=None)|~Q(views__user__id=request.user.id))
        # if show_liked: queryset = queryset.filter(likes__user=request.user)
        return queryset


class HouseProspectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HouseProspect.objects.all()
    serializer_class = HouseProspectSerializer

    filter_backends = [HouseProspectFilter, OrderingFilter]
    ordering_fields = ['zip_location', 'price', 'size', 'rooms', 'post_date']

    @detail_route(methods=['post'])
    def viewed(self, request, **kwargs):
        house = self.get_object()
        user = request.user
        hviews = HouseView.objects.filter(house=house, user=user)
        if hviews.count() == 0:
            house.viewed.add(user)
            hviews = HouseView.objects.filter(house=house, user=user)
        locale.setlocale(locale.LC_ALL, house.advertiser.locale_name)
        viewed_date = hviews[0].view_date.strftime("%d %b %Y")
        return Response(data={"viewed_date": viewed_date })

    @detail_route(methods=['post'])
    def liked(self, request, **kwargs):
        house = self.get_object()
        user = request.user
        hlikes = house.liked.filter(pk=user.id)

        if hlikes.count() == 0:
            house.liked.add(user)
            liked = True
        else:
            house.liked.remove(user)
            liked = False
        return Response(data={"liked": liked})


class IndexView(TemplateView):
    template_name = "housing/housing_index.html"

    def get(self, request, *args, **kwargs):
        advertisers = Advertiser.objects.all()
        return render(request, self.template_name, {"advertisers": advertisers})
