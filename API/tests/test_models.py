import pytest

from API import models

pytestmark = pytest.mark.django_db


def test_road_model():
    """Test the road string representation"""
    road = models.RoadName.objects.create(name="magdalen_road")

    assert str(road) == road.name


def test_direction_model():
    direction = models.Direction.objects.create(name="east")
    assert str(direction) == direction.name


def test_date_model():
    """Test the date string representation"""
    date = models.Date.objects.create(year="1990")
    assert str(date) == date.year


def test_category_model():
    cat = models.Category.objects.create(name="e")
    assert str(cat) == cat.name


def test_StartJunction_model():
    start_junction = models.StartJunction.objects.create(name="not_a_road")
    assert str(start_junction) == start_junction.name


def test_EndJunction_model():
    end_junction = models.EndJunction.objects.create(name="not_a_road")
    assert str(end_junction) == end_junction.name


def test_BasicCountMethod_model():
    basic_count_method = models.BasicCountMethod.objects.create(
        method="not_a_road"
    )
    assert str(basic_count_method) == basic_count_method.method


def test_DetailedCountMethod_model():
    detailed_count_method = models.DetailedCountMethod.objects.create(
        method="not_a_road"
    )
    assert str(detailed_count_method) == detailed_count_method.method


def test_roadinfo_model():
    road = models.RoadName.objects.create(name="magdalen_road")
    cat = models.Category.objects.create(name="e")
    start_junction = models.StartJunction.objects.create(name="not_a_road")
    junc_end = models.EndJunction.objects.create(name="not_a_road")
    direction = models.Direction.objects.create(name="east")
    roadinfo = models.RoadInfo.objects.create(
        road=road,
        category=cat,
        direction=direction,
        junc_start=start_junction,
        junc_end=junc_end,
        len_mi=1,
        len_km=1.6,
    )
    assert str(roadinfo.road.name) == road.name
    assert str(roadinfo.junc_start.name) == start_junction.name
    assert str(roadinfo.junc_end.name) == junc_end.name
    assert str(roadinfo.category.name) == cat.name
    assert str(roadinfo.len_mi) == str(1)
    assert str(roadinfo.len_km) == str(1.6)
    assert str(roadinfo.direction) == direction.name


def test_location_model():
    location = models.Location.objects.create(
        count_point_ref=1, easting=1, latitude=9, northing=12, longitude=12
    )
    assert str(location) == "ref: 1 (9, 12)"


def test_CountMethod_model():

    basic_count_method = models.BasicCountMethod.objects.create(
        method="not_a_road"
    )
    detailed_count_method = models.DetailedCountMethod.objects.create(
        method="not_a_road_detailed"
    )
    count_method = models.CountMethod.objects.create(
        basic_count_method=basic_count_method,
        detailed_count_method=detailed_count_method,
    )
    assert str(count_method) == "NOT_A_ROAD: not_a_road_detailed"


def test_record_model():
    road = models.RoadName.objects.create(name="magdalen_road")
    cat = models.Category.objects.create(name="e")
    start_junction = models.StartJunction.objects.create(name="not_a_road")
    junc_end = models.EndJunction.objects.create(name="not_a_road")
    direction = models.Direction.objects.create(name="east")
    roadinfo = models.RoadInfo.objects.create(
        road=road,
        category=cat,
        direction=direction,
        junc_start=start_junction,
        junc_end=junc_end,
        len_mi=1,
        len_km=1.6,
    )
    date = models.Date.objects.create(year=1990)
    basic_count_method = models.BasicCountMethod.objects.create(
        method="not_a_road"
    )
    detailed_count_method = models.DetailedCountMethod.objects.create(
        method="not_a_road_detailed"
    )
    direction = models.Direction.objects.create(name="east")
    roadinfo = models.RoadInfo.objects.create(
        road=road,
        category=cat,
        direction=direction,
        junc_start=start_junction,
        junc_end=junc_end,
        len_mi=1,
        len_km=1.6,
    )
    count_method = models.CountMethod.objects.create(
        basic_count_method=basic_count_method,
        detailed_count_method=detailed_count_method,
    )
    location = models.Location.objects.create(
        count_point_ref=1, easting=1, latitude=9, northing=12, longitude=12
    )
    record = models.Record.objects.create(
        road=roadinfo, date=date, count_method=count_method, location=location
    )

    assert str(record) == "1990: magdalen_road"


def test_count_model():
    road = models.RoadName.objects.create(name="magdalen_road")
    cat = models.Category.objects.create(name="e")
    start_junction = models.StartJunction.objects.create(name="not_a_road")
    junc_end = models.EndJunction.objects.create(name="not_a_road")
    direction = models.Direction.objects.create(name="east")
    roadinfo = models.RoadInfo.objects.create(
        road=road,
        category=cat,
        direction=direction,
        junc_start=start_junction,
        junc_end=junc_end,
        len_mi=1,
        len_km=1.6,
    )
    date = models.Date.objects.create(year=1990)
    basic_count_method = models.BasicCountMethod.objects.create(
        method="not_a_road"
    )
    detailed_count_method = models.DetailedCountMethod.objects.create(
        method="not_a_road_detailed"
    )
    count_method = models.CountMethod.objects.create(
        basic_count_method=basic_count_method,
        detailed_count_method=detailed_count_method,
    )
    location = models.Location.objects.create(
        count_point_ref=1, easting=1, latitude=9, northing=12, longitude=12
    )
    record = models.Record.objects.create(
        road=roadinfo, date=date, count_method=count_method, location=location
    )
    all_hgvs = 123
    all_motor_vehicles = 2
    pedal_cycles = 3
    two_wheeled_motor_vehicles = 3
    cars_and_taxis = 3
    buses_and_coaches = 3
    lgvs = 3
    hgvs_2_rigid_axle = 3
    hgvs_3_rigid_axle = 3
    hgvs_4_or_more_rigid_axle = 3
    hgvs_3_or_4_articulated_axle = 3
    hgvs_5_articulated_axle = 3
    hgvs_6_articulated_axle = 3

    count = models.Count.objects.create(
        record=record,
        all_hgvs=all_hgvs,
        all_motor_vehicles=all_motor_vehicles,
        pedal_cycles=pedal_cycles,
        two_wheeled_motor_vehicles=two_wheeled_motor_vehicles,
        cars_and_taxis=cars_and_taxis,
        buses_and_coaches=buses_and_coaches,
        lgvs=lgvs,
        hgvs_2_rigid_axle=hgvs_2_rigid_axle,
        hgvs_3_rigid_axle=hgvs_3_rigid_axle,
        hgvs_4_or_more_rigid_axle=hgvs_4_or_more_rigid_axle,
        hgvs_3_or_4_articulated_axle=hgvs_3_or_4_articulated_axle,
        hgvs_5_articulated_axle=hgvs_5_articulated_axle,
        hgvs_6_articulated_axle=hgvs_6_articulated_axle,
    )
    assert count.hgvs_2_rigid_axle == hgvs_2_rigid_axle
