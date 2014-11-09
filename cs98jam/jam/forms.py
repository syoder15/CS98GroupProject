from django import forms

class UploadFileForm(forms.Form):
    filep = forms.FileField()