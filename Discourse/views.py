from django.shortcuts import render, redirect
from django.urls import reverse
from .models import RamblerSub, RamblerPost, RamblerComment
from .forms import RamblerSubForm, RamblerPostForm, RamblerCommentForm
import Website.views as wv
# Create your views here.
class RamblerSubView(wv.RamblerModelContextMixin, wv.RamblerBaseView):
    url_route = 'Discourse/all_subs.html'

    def map_template_name(self, **kwargs):
        return {
            "rambler_forum": RamblerSub.objects.all(),
            "sub_id": self.kwargs.get("sub_id")
        }


class RamblerPostView(wv.RamblerModelContextMixin, wv.RamblerBaseView):
    url_route = 'Discourse/rambler_sub.html'

    def map_template_name(self, **kwargs):
        return {
            "rambler_sub": RamblerSub.objects.get(id=self.kwargs.get("sub_id")),
            "sub_id": self.kwargs.get("sub_id")
        }


class RamblerCommentView(wv.RamblerModelContextMixin, wv.RamblerBaseView):
    url_route = 'Discourse/rambler_post.html'

    def map_template_name(self, **kwargs):
        return {
            "rambler_sub": RamblerSub.objects.get(id=self.kwargs.get("sub_id")),
            "rambler_post": RamblerPost.objects.get(id=self.kwargs.get("post_id")),
            "sub_id": self.kwargs.get("sub_id"),
            "post_id": self.kwargs.get("post_id")
        }


class CreateSubView(wv.RamblerBaseCreateView):
    url_route = 'Discourse/create_sub.html'
    template_form = RamblerSubForm
    model = RamblerSub

    def get_related_models(self, **kwargs):
        return {
            "user": self.request.user
        }


class CreatePostView(wv.RamblerBaseCreateView):
    url_route = 'Discourse/create_post.html'
    template_form = RamblerPostForm
    model = RamblerPost

    def get_success_url(self, **kwargs):
        return reverse('rambler_sub', kwargs=kwargs)

    def get_related_models(self, **kwargs):
        return {
            "user": self.request.user,
            "parent": RamblerSub.objects.get(id=kwargs.get("sub_id"))
        }


class CreateCommentView(wv.RamblerBaseCreateView):
    url_route = 'Discourse/create_comment.html'
    template_form = RamblerCommentForm
    model = RamblerComment

    def get_success_url(self, **kwargs):
        return reverse('rambler_post', kwargs=kwargs)

    def get_related_models(self, **kwargs):
        return {
            "user": self.request.user,
            "parent": RamblerPost.objects.get(id=kwargs.get("post_id"))
        }
