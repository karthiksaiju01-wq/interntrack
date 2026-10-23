from django.urls import path
from . import views

app_name = "tracker"
urlpatterns = [
    path("", views.ApplicationList.as_view(), name="list"),
    path("new/", views.ApplicationCreate.as_view(), name="new"),
    path("<int:pk>/edit/", views.ApplicationUpdate.as_view(), name="edit"),
    path("<int:pk>/delete/", views.ApplicationDelete.as_view(), name="delete"),
]
