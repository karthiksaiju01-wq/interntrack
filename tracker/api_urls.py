from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import ApplicationViewSet

router = DefaultRouter()
router.register("applications", ApplicationViewSet, basename="application")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
]
