from django.contrib.auth.models import User
from django.db import models


class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return f"{self.x:.2f}, {self.y:.2f}"


class Map(models.Model):
    name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="maps/")

    def __str__(self):
        return self.name + " - uploaded by " + str(self.uploaded_by)


class Scaling(models.Model):
    map = models.OneToOneField(Map, related_name="scaling", on_delete=models.CASCADE)
    point1 = models.ForeignKey(
        Point, related_name="scaling_point1", on_delete=models.CASCADE
    )
    point2 = models.ForeignKey(
        Point, related_name="scaling_point2", on_delete=models.CASCADE
    )
    real_distance = models.FloatField()

    @property
    def map_distance(self):
        return (
            (self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2
        ) ** 0.5

    @property
    def scaling_factor(self):
        return self.real_distance / self.map_distance / 0.48

    def __str__(self):
        return f"{self.scaling_factor:.2f}"


class Route(models.Model):
    class Position(models.TextChoices):
        LEFT = "left"
        RIGHT = "right"

    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    set_by = models.ForeignKey(User, on_delete=models.CASCADE)
    set_time = models.DateTimeField(auto_now_add=True)
    points = models.ManyToManyField(Point, related_name="routes")
    number_of_angles = models.IntegerField()
    position = models.CharField(
        max_length=10,
        choices=[(tag.name, tag.value) for tag in Position],
    )

    def start(self):
        return self.points.first()

    def end(self):
        return self.points.last()

    def __str__(self):
        return f"Route {self.id} - {self.set_by.username} - {self.set_time}"


class Problem(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    start = models.ForeignKey(
        Point, related_name="problem_start", on_delete=models.CASCADE
    )
    end = models.ForeignKey(Point, related_name="problem_end", on_delete=models.CASCADE)
    routes = models.ManyToManyField(Route, related_name="problems")

    @property
    def complex(self):
        return len(self.routes) > 2


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    problems = models.ManyToManyField(Problem, related_name="projects")

    def __str__(self):
        return self.name + " - created by " + str(self.created_by)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    choice = models.ForeignKey(Route, related_name="votes", on_delete=models.CASCADE)
    reaction_time_seconds = models.FloatField()
    vote_time = models.DateTimeField(auto_now_add=True)
