from django import forms
from posts.models import Posts, Tags, Images


class CreatePost(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['comments']


class CreateImage(forms.ModelForm):
    image = forms.FileField(widget=forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }))

    class Meta:
        model = Images
        fields = ['image']


class CreateTags(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['tags']
