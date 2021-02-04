from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from UserBase.models import User, Profile
from Discourse.models import RamblerSub, RamblerPost, RamblerComment

# Create your views here.
class RamblerBaseContextMixin:
    def get_context_data(self, **kwargs):
        context = {
            "user": self.request.user,
        }
        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(profile_user=self.request.user)
        else:
            context["profile"] = self.request.user #anonymous user

        return context


class RamblerModelContextMixin(RamblerBaseContextMixin):
    """
    """
    def get_context_data(self, **kwargs):
        context = super(RamblerModelContextMixin, self).get_context_data(**kwargs)
        context.update(self.map_template_name(**kwargs))#map_template_name returns a dict mapping template names to corresponding models
        return context

    def map_template_name(self, **kwargs):
        """
        called in get_context_data.
        offers additional context that uses the url arguments
        """
        return dict()


class RamblerFormContextMixin(RamblerModelContextMixin):
    """
    Requires inheriting class to have as additional attributes:
        - template_form: forms.Form instance
    """
    def get_context_data(self, **kwargs):
        context = super(RamblerFormContextMixin, self).get_context_data(**kwargs)
        if "form" in kwargs:
            context["form"] = kwargs["form"]
        else:
            context["form"] = self.template_form()
        return context


class RamblerBaseFormMixin:
    def get_related_models(self, **kwargs):
        return dict()

    def process_form(self, form, model, **related):
        related.update(**form.cleaned_data)
        created = model(**related)
        created.save()


class RamblerBaseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, self.url_route, self.get_context_data(**kwargs))


@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class LogReqRamblerBaseView(RamblerBaseView):
    pass


class RamblerBaseFormView(RamblerFormContextMixin, RamblerBaseFormMixin, RamblerBaseView):
    """
    Used for creating objects of a specific model, requires the inheriting view
    to have as attributes:
        - url_route
        - model: models.Model
        - template_form
    """
    def get_success_url(self, **kwargs):
        return '/'

    def post(self, request, *args, **kwargs):
        form = self.template_form(request.POST)
        if form.is_valid():
            self.process_form(form, self.model, **self.get_related_models(**kwargs))
            return redirect(self.get_success_url(**kwargs))

        return render(request, self.url_route, self.get_context_data(**kwargs))


@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class RamblerBaseCreateView(RamblerBaseFormView):
    """
    Used for creating objects of a specific model, requires the inheriting view
    to have as attributes:
        - url_route
        - model: models.Model
        - template_form
    requires user to be logged in to do creation.
    """
    pass


class LandingPageView(RamblerModelContextMixin, RamblerBaseView):
    url_route = 'landing_page.html'

    def map_template_name(self, **kwargs):
        return {
            "default_subs": RamblerSub.objects.all(),
            "trending_posts": RamblerPost.objects.all(),
        }


class DoodleView(RamblerModelContextMixin, LogReqRamblerBaseView):
    url_route = 'doodle.html'

    def map_template_name(self, **kwargs):
        return {
            "subs": RamblerSub.objects.all(),
            "posts": RamblerPost.objects.all(),
            "comments": RamblerComment.objects.all(),
            "current_sub": RamblerSub.objects.get(id=2),
            "kwargs": kwargs
        }
