from django import forms

class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    # Add other fields as needed
