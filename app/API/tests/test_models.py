from unittest.mock import patch

import pytest


from API import models

pytestmark = pytest.mark.django_db




def test_road_model():
    """Test the road string representation"""
    road = models.RoadName.objects.create(name="magdalen")
    
    assert str(road) == road.name

def test_date_model():
    """Test the date string representation"""
    date = models.Date.objects.create(name=1990)
    assert str(date) == date.year



# def test_ingredient_str():
#     """Test the ingredient string representation"""
#     ingredient = models.Ingredient.objects.create(
#         user=sample_user(), name="Fennel"
#     )

#     assert str(ingredient) == ingredient.name


# def test_recipe_str():
#     """Test the recipe string representation"""
#     recipe = models.Recipe.objects.create(
#         user=sample_user(), title="pizza", time_minutes=240, price=10.0
#     )

#     assert str(recipe) == recipe.title


# @patch("uuid.uuid4")
# def test_recipe_file_name_uuid(mock_uuid):
#     """Test that image is saved in the correct location"""
#     uuid = "test-uuid"
#     mock_uuid.return_value = uuid
#     file_path = models.recipe_image_file_path(None, "myimage.jpg")
#     exp_path = f"uploads/recipe/{uuid}.jpg"

#     assert file_path == exp_path
