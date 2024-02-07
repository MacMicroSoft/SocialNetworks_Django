from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static
from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('create_posts/', views.create_posts, name='create_posts'),
    path('posts/', views.posts, name='posts'),
    path('user_posts/', views.user_posts, name='user_posts'),
    path('edit_profile/<int:post_id>/', views.edit_profile, name='edit_profile'),
    path('post_like/<int:pk>/', views.post_like, name='post_like'),
]
