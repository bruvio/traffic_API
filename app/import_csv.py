# flake8: noqa
import os

import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traffic_API.settings")
django.setup()


from API.models import (
    BasicCountMethod,
    Category,
    Count,
    CountMethod,
    Date,
    DetailedCountMethod,
    Direction,
    EndJunction,
    Location,
    Record,
    RoadInfo,
    RoadName,
    StartJunction,
)

df = pd.read_csv("data/input_data.csv")


def create_records(num=100):
    """
    create_records populate database with data from csv file

    Parameters
    ----------
    num : int, optional
        defult number of row that are going to be imported, by default 100
    """

    for records, row in enumerate(df.to_dict(orient="records")):
        latitude, longitude = row["latitude"], row["longitude"]

        road_name_obj, _ = RoadName.objects.get_or_create(
            name=row["road_name"]
        )
        date_obj, _ = Date.objects.get_or_create(year=row["year"])
        category_obj, _ = Category.objects.get_or_create(
            name=row["road_category"]
        )
        junc_start_obj, _ = StartJunction.objects.get_or_create(
            name=row["start_junction_road_name"]
        )
        junc_end_obj, _ = EndJunction.objects.get_or_create(
            name=row["end_junction_road_name"]
        )
        bcm_obj, _ = BasicCountMethod.objects.get_or_create(
            method=row["estimation_method"]
        )
        dcm_obj, _ = DetailedCountMethod.objects.get_or_create(
            method=row["estimation_method_detailed"],
        )
        direction_obj, _ = Direction.objects.get_or_create(
            name=row["direction_of_travel"],
        )

        road_obj, _ = RoadInfo.objects.get_or_create(
            road=road_name_obj,
            category=category_obj,
            direction=direction_obj,
            junc_start=junc_start_obj,
            junc_end=junc_end_obj,
            len_mi=row["link_length_miles"],
            len_km=row["link_length_km"],
        )
        location_obj, _ = Location.objects.get_or_create(
            count_point_ref=row["count_point_id"],
            easting=row["easting"],
            latitude=latitude,
            northing=row["northing"],
            longitude=longitude,
        )
        count_method_obj, _ = CountMethod.objects.get_or_create(
            basic_count_method=bcm_obj,
            detailed_count_method=dcm_obj,
        )
        record_obj, _ = Record.objects.get_or_create(
            road=road_obj,
            date=date_obj,
            count_method=count_method_obj,
            location=location_obj,
        )
        count_obj, _ = Count.objects.get_or_create(
            record=record_obj,
            all_hgvs=row["all_hgvs"],
            all_motor_vehicles=row["all_motor_vehicles"],
            pedal_cycles=row["pedal_cycles"],
            two_wheeled_motor_vehicles=row["two_wheeled_motor_vehicles"],
            cars_and_taxis=row["cars_and_taxis"],
            buses_and_coaches=row["buses_and_coaches"],
            lgvs=row["lgvs"],
            hgvs_2_rigid_axle=row["hgvs_2_rigid_axle"],
            hgvs_3_rigid_axle=row["hgvs_3_rigid_axle"],
            hgvs_4_or_more_rigid_axle=row["hgvs_4_or_more_rigid_axle"],
            hgvs_3_or_4_articulated_axle=row["hgvs_3_or_4_articulated_axle"],
            hgvs_5_articulated_axle=row["hgvs_5_articulated_axle"],
            hgvs_6_articulated_axle=row["hgvs_6_articulated_axle"],
        )

        print(
            "row n {} longitude {}, latitude{}".format(
                records, longitude, latitude
            )
        )
        if num and records == num:
            break


create_records()
