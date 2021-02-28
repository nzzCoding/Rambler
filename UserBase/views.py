from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse_lazy, reverse
from .models import Profile
from .forms import RegisterForm, LoginForm, ProfileEditForm
import Website.views as wv

# Create your views here.
User = get_user_model()

class LoginView(wv.RamblerBaseFormView):
    url_route = 'UserBase/login.html'
    template_form = LoginForm
    model = User
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.template_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            auth_user = authenticate(request, username=username, password=password)
            if auth_user != None:
                login(request, auth_user)
                return redirect(self.success_url)
            else:
                form.add_error(None, "Authentication failed")
        kwargs["form"] = form#used in self.get_context_data(**kwargs), refer to RamblerFormContextMixin
        return render(request, self.url_route, self.get_context_data(**kwargs))


class RegisterView(wv.RamblerBaseFormView):
    url_route = 'UserBase/register.html'
    template_form = RegisterForm
    model = User
    success_url = reverse_lazy('own_profile')

    def post(self, request, *args, **kwargs):
        form = self.template_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            User.objects.create_user(username=username, password=password)
            auth_user = authenticate(request, username=username, password=password)
            login(request, auth_user)
            return redirect(self.success_url)
        kwargs["form"] = form#used in self.get_context_data(**kwargs), refer to RamblerFormContextMixin
        return render(request, self.url_route, self.get_context_data(**kwargs))


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('/')

class ProfileEditView(wv.RamblerBaseContextMixin, wv.LogReqRamblerBaseView):
    url_route = 'UserBase/profile_edit.html'
    success_url = reverse_lazy('own_profile')

    def post(self, request, *args, **kwargs):
        form = ProfileEditForm(request.POST, request.FILES)
        profile = Profile.objects.get(profile_user=request.user)
        if form.is_valid():
            profile.picture = request.FILES.get("picture")
            profile.save()
            return redirect(self.success_url)
        return render(request, self.url_route, self.get_context_data(**kwargs))


class ProfileDetailView(wv.RamblerModelContextMixin, wv.RamblerBaseView):
    url_route = 'UserBase/profile_overview.html'

    def map_template_name(self, **kwargs):
        return {
            "visited_profile": Profile.objects.get(id=self.kwargs.get("profile_key"))
        }

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logged_profile = self.request.user.profile.id
            visited_profile = kwargs.get("profile_key")

            if logged_profile == visited_profile:
                return redirect(reverse('own_profile'))

        return render(request, self.url_route, self.get_context_data(**kwargs))


class OwnProfileView(wv.RamblerBaseContextMixin, wv.RamblerBaseView):
    url_route = 'UserBase/own_profile_overview.html'
