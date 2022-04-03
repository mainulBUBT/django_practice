from django import forms

class CrudForm(forms.Form):
    name = forms.CharField(label="Enter your name")
    mobile = forms.CharField(label="Enter your mobile number")