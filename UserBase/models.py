from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Profile(models.Model):
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edition_date = models.DateTimeField(auto_now=True)
    picture = models.FileField(blank=True, null=True, upload_to='UserBase')

    def get_comments(self):
        return self.profile_user.comments.all()

    def get_posts(self):
        return self.profile_user.posts.all()

    def get_subs(self):
        return self.profile_user.subs.all()

    def count_comments(self):
        return self.get_comments().count()

    def count_posts(self):
        return self.get_posts().count()

    def count_subs(self):
        return self.get_subs().count()


def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(profile_user=instance)

post_save.connect(create_profile, sender=User)
