from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.templatetags.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.posts, name='posts'),
    path('post/create/', views.create_posts, name='create_posts'),
    path('post/<int:post_id>/edit/', views.edit_posts, name='edit_posts'),
    path('post/<int:pk>/post_like/', views.post_like, name='post_like'),
]
