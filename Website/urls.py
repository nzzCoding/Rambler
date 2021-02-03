from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='main_page'),
    path('doodle/', views.DoodleView.as_view(), name='doodle_view')
]
