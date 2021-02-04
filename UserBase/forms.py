from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    #failure to authenticate is handled in the view


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    confirm  = forms.CharField(max_length=50, widget=forms.PasswordInput)
    email    = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("The username must be at least 3 characters long.")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is not available.")
        return username

    def clean_confirm(self):
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        if len(password) < 4:
            raise forms.ValidationError("Your password must be at least 4 characters long.")
        if password != confirm:
            raise forms.ValidationError("Your passwords are not matching.")
        return confirm

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is not available.")
        return email


class ProfileEditForm(forms.Form):
    picture = forms.FileField(allow_empty_file=True)

    def clean_picture(self):
        #TODO: not implemented yet.
        picture = self.cleaned_data.get("picture")
        return picture
