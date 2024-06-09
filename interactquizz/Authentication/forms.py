from django import forms
from .models import CustomUser


class ProfileImageUpload(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']
