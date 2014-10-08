from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserSignupForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    
    class Meta:
        model = User
        fields = ("username", "email")

    # validate that email address isn't already registered
    def clean_email(self):
    	email = self.cleaned_data["email"]
    	try:
    		user = User.objects.get(email = email)
    		raise forms.ValidationError("This email address is already associated with a JAM account")
    	except User.DoesNotExist:
    		return email
    def save(self, commit=True):
    	user = super(UserCreationForm,self).save(commit = False)
    	user.set_password(self.cleaned_data["password1"])
    	user.email = self.cleaned_data["email"]
    	user.is_active = False
    	if commit:
    		user.save()
    	return user
		

