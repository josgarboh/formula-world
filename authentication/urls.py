

from django.urls import include, path
from authentication import views


urlpatterns = [
    path("register/", views.registro, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),


]