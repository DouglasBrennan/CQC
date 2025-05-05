from django.contrib.auth.models import User
from django.db import models


class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()


class Map(models.Model):
    class Scaling(models.Model):
        point1 = models.ForeignKey(
            Point, related_name="point1", on_delete=models.CASCADE
        )
        point2 = models.ForeignKey(
            Point, related_name="point2", on_delete=models.CASCADE
        )
        real_distance = models.FloatField()

    name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="maps/")
    scaling = models.ForeignKey(
        Scaling, related_name="scaling", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.name + " - uploaded by " + str(self.uploaded_by)


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
        return self.name


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
