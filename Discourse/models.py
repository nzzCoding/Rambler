from django.db import models
from django.conf import settings

# Create your models here.
class RamblerSub(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subs')
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_posts(self):
        return self.posts.all()


class RamblerPost(models.Model):
    user   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    parent = models.ForeignKey(RamblerSub, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=120)
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_sub(self):
        return self.parent

    def get_comments(self):
        return self.comments.all()

    def get_truncated_content(self):
        if len(self.content) < 120:
            return self.content
        else:
            return self.content[:120] + " ..."


class RamblerComment(models.Model):
    user   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(RamblerPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} comment on {self.parent}"

    def get_sub(self):
        return self.parent.parent

    def get_post(self):
        return self.parent
