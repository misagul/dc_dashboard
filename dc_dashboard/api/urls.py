from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cookies/", views.cookies, name="cookies"),
    path("usages/", views.usages, name="usages"),
    path("login/", views.login_request, name="login")

]
