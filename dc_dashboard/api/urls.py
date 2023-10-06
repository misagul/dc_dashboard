from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "api"

urlpatterns = [
    path("get_channels/", views.get_channels, name="get_channels"),
    path("add_channel/", views.add_channel, name="add_channel"),
    path("update_channel/", views.update_channel, name="update_channel"),
    path("delete_channel/", views.delete_channel, name="delete_channel"),
    path("get_channel_limit/", views.get_channel_limit, name="get_channel_limit"),

    path("get_cookies/", views.get_cookies, name="get_cookies"),
    path("get_current_cookie/", views.get_current_cookie, name="get_current_cookie"),
    path("update_cookie_status/", views.update_cookie_status, name="update_cookie_status"),
    path("add_cookie/", views.add_cookie, name="add_cookie"),
    path("update_cookie/", views.update_cookie, name="update_cookie"),
    path("delete_cookie/", views.delete_cookie, name="delete_cookie"),

    path("get_members/", views.get_members, name="get_members"),
    path("get_member_usage/", views.get_member_usage, name="get_member_usage"),
    path("add_member_usage/", views.add_member_usage, name="add_member_usage"),
    
]
