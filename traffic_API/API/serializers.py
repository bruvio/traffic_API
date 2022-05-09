from rest_framework import serializers

from API.models import Count, CountMethod, Date, Location, Record, RoadInfo


class DateSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()

    class Meta:
        model = Date
        exclude = ("id",)


class RoadSerializer(serializers.ModelSerializer):
    road_name = serializers.CharField()
    road_category = serializers.CharField()
    start_junction_road_name = serializers.CharField()
    end_junction_road_name = serializers.CharField()
    len_mi = serializers.FloatField()
    len_km = serializers.FloatField()

    class Meta:
        model = RoadInfo
        exclude = ("id",)


class LocationSerializer(serializers.ModelSerializer):
    count_point_ref = serializers.IntegerField()
    easting = serializers.IntegerField()
    latitude = serializers.FloatField()
    northing = serializers.IntegerField()
    longitude = serializers.FloatField()

    class Meta:
        model = Location
        exclude = ("id",)


class CountMethodSerializer(serializers.ModelSerializer):
    basic_count_method = serializers.CharField()
    detailed_count_method = serializers.CharField()

    class Meta:
        model = CountMethod
        exclude = ("id",)


class CountSerializer(serializers.ModelSerializer):

    all_hgvs = serializers.IntegerField()
    all_motor_vehicles = serializers.IntegerField()
    pedal_cycles = serializers.IntegerField()
    two_wheeled_motor_vehicles = serializers.IntegerField()
    cars_and_taxis = serializers.IntegerField()
    buses_and_coaches = serializers.IntegerField()
    lgvs = serializers.IntegerField()
    hgvs_2_rigid_axle = serializers.IntegerField()
    hgvs_3_rigid_axle = serializers.IntegerField()
    hgvs_4_or_more_rigid_axle = serializers.IntegerField()
    hgvs_3_or_4_articulated_axle = serializers.IntegerField()
    hgvs_5_articulated_axle = serializers.IntegerField()
    hgvs_6_articulated_axle = serializers.IntegerField()

    class Meta:
        model = Count
        exclude = ("id", "record")


class RecordSerializer(serializers.ModelSerializer):
    road = RoadSerializer()
    date = DateSerializer()
    count_method = CountMethodSerializer()
    location = LocationSerializer()
    count = CountSerializer()

    class Meta:
        model = Record
        exclude = ("id",)
