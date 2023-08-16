from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "api"

urlpatterns = [
    path("delete_channel/", login_required(views.delete_channel), name="delete_channel"),
    path("add_channel/", login_required(views.add_channel), name="add_channel"),
]
