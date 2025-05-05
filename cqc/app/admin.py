from django.contrib import admin

from .models import Map, Point, Problem, Route


# Register your models here.
@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ("name", "uploaded_by", "upload_time")
    search_fields = ("name", "uploaded_by__username")
    list_filter = ("upload_time",)
    ordering = ("-upload_time",)


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ("x", "y")
    search_fields = ("x", "y")
    ordering = ("x", "y")
    list_per_page = 10


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("map", "set_by", "set_time", "number_of_angles", "position")
    search_fields = ("map__name", "set_by__username")
    list_filter = ("set_time", "position")
    ordering = ("-set_time",)
    list_per_page = 10
    date_hierarchy = "set_time"


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("map", "start", "end")
    search_fields = ("map__name", "start__x", "start__y")
    list_filter = ("map",)
    ordering = ("map",)
    list_per_page = 10
