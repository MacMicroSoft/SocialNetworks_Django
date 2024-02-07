from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from posts.forms import CreateImage, CreatePost, CreateTags
from posts.models import Images, Posts, Tags


@login_required
def create_posts(request):
    if request.method == 'POST':
        form = CreatePost(request.POST)
        tags_form = CreateTags(request.POST)
        image_form = CreateImage(request.POST, request.FILES)

        if form.is_valid() and tags_form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()

            # Handle images
            files = request.FILES.getlist('image')
            for image in files:
                image, created = Images.objects.get_or_create(image=image)
                post.images.add(image)

            # Handle tags
            tags_input = tags_form.cleaned_data['tags']
            for tag in tags_input.split(' '):
                tag, created = Tags.objects.get_or_create(tags=tag)
                post.tags.add(tag)

            messages.success(request, "Post created successfully!")
            return redirect('profile', user_id=request.user.profile.id)
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")
    else:
        form = CreatePost()
        tags_form = CreateTags()
        image_form = CreateImage()

    context = {'form': form, 'tags_form': tags_form, 'image_form': image_form}
    return render(request, 'posts/create_posts.html', context)


@login_required
def posts(request):
    posts_date = Posts.objects.all().order_by('-date').select_related('user__user').prefetch_related('images', 'tags', 'like')

    return render(request, 'posts/posts.html', {'posts_date': posts_date})


@login_required
def user_posts(request):
    user_profile = request.user.profile
    user_posts = Posts.objects.filter(user=user_profile)

    return render(request, 'posts/create_posts.html', {'user_posts': user_posts})


@login_required
def edit_profile(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    if request.method == 'POST':
        tags_form = CreateTags(request.POST)
        if tags_form.is_valid():
            tags_input = tags_form.cleaned_data['tags']
            for tag_name in tags_input.split(' '):
                tag, created = Tags.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
            messages.success(request, "Tags edited successfully!")
            return redirect('user_posts', post_id=post.id)
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")
    else:
        tags_form = CreateTags()

    context = {'tags_form': tags_form}
    return render(request, 'posts/edit_profile.html', context)


@login_required
def post_like(request, pk):
    post = get_object_or_404(Posts, id=pk)
    if request.user.profile in post.like.all():
        post.like.remove(request.user.profile)
    else:
        post.like.add(request.user.profile)

    return redirect('posts')
