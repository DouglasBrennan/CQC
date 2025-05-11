from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.forms import MapUploadForm, ScalingForm
from app.models import Map, Point, Project, Scaling

# Create your views here.


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def map_selection(request):
    context = dict()
    if request.method == "POST":
        map_upload_form = MapUploadForm(request.POST, request.FILES)
        if map_upload_form.is_valid():
            # Process the uploaded file
            uploaded_file = request.FILES["map_file"]
            # create a new Map instance
            map = Map(
                name=map_upload_form.cleaned_data["map_name"],
                uploaded_by=request.user,
                file=uploaded_file,
            )
            # Save the map instance to the database
            map.save()
            # Redirect to a success page or render a success message
            return redirect("map_selection")
        else:
            errors = map_upload_form.errors
            context["errors"] = errors
            context["map_upload_form"] = map_upload_form
            return render(request, "map_selection.html", context)

    context["map_upload_form"] = MapUploadForm()
    maps = Map.objects.all()
    context["maps"] = maps
    return render(request, "map_selection.html", context)


@login_required
def set_scaling(request, map_id=None):
    map = Map.objects.get(id=map_id)
    if request.method == "POST":
        point1_x = request.POST.get("point1_x")
        point1_y = request.POST.get("point1_y")
        point2_x = request.POST.get("point2_x")
        point2_y = request.POST.get("point2_y")
        real_distance = request.POST.get("real_distance")

        if map.scaling:
            scaling = map.scaling
            scaling.point1.x = point1_x
            scaling.point1.y = point1_y
            scaling.point2.x = point2_x
            scaling.point2.y = point2_y
            scaling.real_distance = real_distance
            scaling.point1.save()
            scaling.point2.save()
        else:
            scaling = Scaling(map=map)
            scaling.point1 = Point(x=point1_x, y=point1_y)
            scaling.point2 = Point(x=point2_x, y=point2_y)
            scaling.real_distance = real_distance
            scaling.point1.save()
            scaling.point2.save()
            scaling.map = map

        scaling.save()
        return redirect("map_selection")
    context = dict()
    context["map"] = map
    if map.scaling:
        scaling_form = ScalingForm(scaling_instance=map.scaling)
    else:
        scaling_form = ScalingForm()
    context["scaling_form"] = scaling_form

    return render(request, "set_scaling.html", context)


@login_required
def course_setting(request, map_id=None):
    map = Map.objects.get(id=map_id)
    projects = Project.objects.filter(map=map)
    context = {
        "map": map,
        "projects": projects,
    }
    return render(request, "course_setting.html", context)


@login_required
def route_choice(request):
    return render(request, "route_choice.html")
