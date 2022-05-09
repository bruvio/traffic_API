"""traffic_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]


from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from API import views

router = DefaultRouter()
router.get_api_root_view().cls.__doc__ = '<a href="{}">A (Django) RESTful API providing traffic data count and major road data.</a>'.format(
    "https://github.com/bruvio/traffic_API"
)

router.register(r"count", views.CountViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
]
