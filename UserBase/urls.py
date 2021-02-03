from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.OwnProfileView.as_view(), name='own_profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('<int:profile_key>/details/', views.ProfileDetailView.as_view(), name='profile_detail'),
]
