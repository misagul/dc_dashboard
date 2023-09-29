from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("cookies/", login_required(views.cookies), name="cookies"),
    path("members/", login_required(views.members), name="members"),
    path("channels/", login_required(views.channels), name="channels"),
    path("login/", views.login_request, name="login"),
    path("logout/", login_required(views.logout_request), name='logout'),

]
