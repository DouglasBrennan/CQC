from django.urls import path

import app.views as views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("map_selection/", views.map_selection, name="map_selection"),
    path("set_scaling/<int:map_id>/", views.set_scaling, name="set_scaling"),
    path("course_setting/<int:map_id>/", views.course_setting, name="course_setting"),
    path("route_choice/", views.route_choice, name="route_choice"),
]
