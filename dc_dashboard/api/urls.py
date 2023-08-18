from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "api"

urlpatterns = [
    path("get_channels/", views.get_channels, name="get_channels"),
    path("add_channel/", views.add_channel, name="add_channel"),
    path("update_channel/", views.update_channel, name="update_channel"),
    path("delete_channel/", views.delete_channel, name="delete_channel"),

    path("get_cookies/", views.get_cookies, name="get_cookies"),
    path("add_cookie/", views.add_cookie, name="add_cookie"),
    path("update_cookie/", views.update_cookie, name="update_cookie"),
    path("delete_cookie/", views.delete_cookie, name="delete_cookie"),
]
