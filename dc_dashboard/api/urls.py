from django.urls import path
from . import views

appname = "api"

urlpatterns = [
    path("delete_channel/<int:channel_id>/", views.delete_channel, name="delete_channel"),
]
