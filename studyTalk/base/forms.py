from django import forms
from .models import Room
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields='__all__'
        exclude=['host','participants']



class RegistrationForm(UserCreationForm):
    # Email = forms.EmailField( required=True)

    class Meta:
        model=User
        fields=['username','email','password1','password2']


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']