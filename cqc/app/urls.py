from django.urls import path

from app.views import (
    course_setting,
    index,
    login_view,
    logout_view,
    map_selection,
    route_choice,
)

urlpatterns = [
    path("", index, name="index"),
    path("accounts/login/", login_view, name="login"),
    path("accounts/logout/", logout_view, name="logout"),
    path("course_setting/<int:map_id>/", course_setting, name="course_setting"),
    path("map_selection/", map_selection, name="map_selection"),
    path("route_choice/", route_choice, name="route_choice"),
]
