from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from users import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/follow/<int:user_id>/', views.profile_follow, name='follow'),
    path('profile/followers/<int:user_id>/', views.profile_followers, name='followers'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
