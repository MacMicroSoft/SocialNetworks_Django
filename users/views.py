from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from posts.models import Images, Posts, Tags
from users.forms import LoginForm, ProfileForm, RegisterForm, UpdateUserForm
from users.models import Profile
from users.tokens import account_activation_token


def home(request):
    return render(request, 'base.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile_settings')
    else:
        return HttpResponse('Activation link is invalid!')


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('profile', user_id=request.user.profile.id)
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request, user_id):
    profile_date = get_object_or_404(Profile, id=user_id)

    if request.method == 'POST':
        profile_to_follow = profile_date

        if request.user.profile != profile_to_follow:
            if request.user.profile.follows.filter(id=user_id).exists():
                request.user.profile.follows.remove(profile_to_follow)
            else:
                request.user.profile.follows.add(profile_to_follow)

        return redirect('profile', user_id=profile_date.id)

    is_following = request.user.profile.follows.filter(id=user_id).exists()

    user_date = profile_date.id
    post_date = Posts.objects.filter(user_id=user_date).prefetch_related('images', 'tags')

    return render(request, 'users/profile.html', {'post_date': post_date, 'profile_date': profile_date, 'is_following': is_following})


@login_required
def profile_settings(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")

    else:
        user_form = ProfileForm(instance=request.user)
        profile_form = UpdateUserForm(instance=request.user.profile)

    return render(request, 'users/profile_settings.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def profile_follow(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)

    followers = profile.followed_by.all()
    following = profile.follows.all()

    if request.method == 'POST':
        if request.user.profile != profile:
            if request.user.profile.follows.filter(id=user_id).exists():
                request.user.profile.follows.remove(profile)
                return redirect('follow', user_id=request.user.profile.id)

    return render(request, 'users/follow.html', {'profile': profile, 'following': following})


def profile_followers(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)

    followers = profile.followed_by.all()

    return render(request, 'users/followers.html', {'profile': profile, 'followers': followers})
