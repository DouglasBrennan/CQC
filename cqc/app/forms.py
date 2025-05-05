from django import forms


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
