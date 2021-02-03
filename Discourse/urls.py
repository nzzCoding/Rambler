from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.RamblerSubView.as_view()),
    path('create/', views.CreateSubView.as_view(), name='create_sub'),
    path('<int:sub_id>/', include([
        path('', views.RamblerPostView.as_view(), name='rambler_sub'),
        path('create/', views.CreatePostView.as_view(), name='create_post'),
        path('post/<int:post_id>/', include([
            path('', views.RamblerCommentView.as_view(), name='rambler_post'),
            path('create/', views.CreateCommentView.as_view(), name='create_comment'),
            ])),
        ])
    ),
]
