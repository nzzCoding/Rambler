# Generated by Django 3.1.2 on 2021-01-25 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RamblerSub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RamblerPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('content', models.TextField()),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('edited', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='Discourse.ramblersub')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RamblerComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('edited', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Discourse.ramblerpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
