from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import viewsets

from API.models import Record
from API.serializers import RecordSerializer


class CountViewSet(viewsets.ReadOnlyModelViewSet):
    """List of all traffic count Counts"""

    queryset = Record.objects.all().select_related("count")
    serializer_class = RecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "road",
        "date",
        "count_method",
        "count_method_basic_count_method",
        "count_method_detailed_count_method",
        "location",
        "road_category",
        "road_junc_start",
        "road_junc_end",
        "road_road__name",
        "date_year",
        "location_count_point_ref",
        "road_category__name",
        "road_junc_start__name",
        "road_junc_end__name",
    )
