from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.templatetags.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('posts/create/', views.create_posts, name='create_posts'),
    path('posts/<int:post_id>/edit/', views.edit_posts, name='edit_posts'),
    path('posts/<int:pk>/post_like/', views.post_like, name='post_like'),
]
