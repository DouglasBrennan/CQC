from django import forms
from django.utils.safestring import mark_safe

from app.models import Scaling


class MapUploadForm(forms.Form):
    map_file = forms.ImageField(
        label="Upload Map Image",
        required=True,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )
    map_name = forms.CharField(
        label="Map Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class ScalingForm(forms.Form):
    point1_x = forms.FloatField(
        required=True,
        widget=forms.NumberInput(),
    )
    point1_y = forms.FloatField(
        required=True,
        widget=forms.NumberInput(),
    )
    point2_x = forms.FloatField(
        required=True,
        widget=forms.NumberInput(),
    )
    point2_y = forms.FloatField(
        required=True,
        widget=forms.NumberInput(),
    )
    map_distance = forms.FloatField(
        label="Map Distance",
        required=True,
        disabled=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    real_distance = forms.FloatField(
        label="Real Distance (<a href='https://maps.google.com/' target='_blank' rel='noopener noreferrer'>measure</a>)",
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, scaling_instance: Scaling = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["real_distance"].label = mark_safe(
            self.fields["real_distance"].label
        )
        if scaling_instance:
            self.fields["point1_x"].initial = scaling_instance.point1.x
            self.fields["point1_y"].initial = scaling_instance.point1.y
            self.fields["point2_x"].initial = scaling_instance.point2.x
            self.fields["point2_y"].initial = scaling_instance.point2.y
            self.fields["map_distance"].initial = scaling_instance.map_distance
            self.fields["real_distance"].initial = scaling_instance.real_distance
