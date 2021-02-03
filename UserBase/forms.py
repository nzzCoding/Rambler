from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    confirm  = forms.CharField(max_length=50, widget=forms.PasswordInput)
    email    = forms.EmailField()

    """def clean_username(self):
        pass

    def clean_confirm(self):
        pass

    def clean_email(self):
        pass"""


class ProfileEditForm(forms.Form):
    picture = forms.FileField(allow_empty_file=True)
