from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    
    class Meta:
        model = User
        fields = ("username", "email")
