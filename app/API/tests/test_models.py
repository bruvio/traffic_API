import pytest

from API import models

pytestmark = pytest.mark.django_db


def test_road_model():
    """Test the road string representation"""
    road = models.RoadName.objects.create(name="magdalen_road")

    assert str(road) == road.name


def test_date_model():
    """Test the date string representation"""
    date = models.Date.objects.create(year="1990")
    assert str(date) == date.year


def test_category_model():
    cat = models.Category.objects.create(name="not_a_road")
    assert str(cat) == cat.name


def test_StartJunction_model():
    StartJunction = models.StartJunction.objects.create(name="not_a_road")
    assert str(StartJunction) == StartJunction.name


def test_EndJunction_model():
    EndJunction = models.EndJunction.objects.create(name="not_a_road")
    assert str(EndJunction) == EndJunction.name


def test_BasicCountMethod_model():
    BasicCountMethod = models.BasicCountMethod.objects.create(
        method="not_a_road"
    )
    assert str(BasicCountMethod) == BasicCountMethod.method


def test_DetailedCountMethod_model():
    DetailedCountMethod = models.DetailedCountMethod.objects.create(
        method="not_a_road"
    )
    assert str(DetailedCountMethod) == DetailedCountMethod.method
