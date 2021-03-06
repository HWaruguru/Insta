from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from insta.email import send_welcome_email
from .models import Post, Comment, Profile, Follow
from insta.forms import CommentForm, PostForm, SignUpForm, UpdateUserForm, UpdateUserProfileForm


@login_required(login_url='/accounts/login/')
def index(request):
    followers = Follow.objects.filter(follower=request.user.profile)
    follows = Profile.objects.exclude(id__in=[follower.followed.id for follower in followers]).exclude(id=request.user.profile.id)[:5]
    posts = Post.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            print('\n\n')
            print(post)
            print('\n\n')
            post.profile = request.user.profile
            post.save()
            print("Hello, Hellooo, who is here.!")
            return HttpResponseRedirect(request.path_info)
    else:
        print("This form does not work!")
        form = PostForm()

    return render(request, "index.html", {"posts": posts, "follows": follows, "form": form})

def follow(request, followed_id):
    if request.method == 'GET':
        try:
            followed = Profile.objects.get(pk=followed_id)
            follow = Follow(follower=request.user.profile, followed=followed)
            follow.save()
        except IntegrityError as e:
            pass
    return redirect('index')

@login_required(login_url='login')
def profile(request):
    posts = request.user.profile.posts.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {"posts": posts, 'user_form': user_form, 'prof_form': prof_form})

@login_required(login_url='login')
def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.post = post
            savecomment.profile = request.user.profile
            savecomment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    return render(request, 'post.html', {"post": post, "form": form})

def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'GET':
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            send_welcome_email(user.username, user.email)

            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})


@login_required(login_url='login')
def search_posts(request):
    if 'user' in request.GET and request.GET['user']:
        username = request.GET.get("user")
        posts = Post.objects.filter(profile__user__username__icontains=username)
        if len(posts) > 0:
            return render(request, 'search_result.html', {"posts": posts})
    return redirect('index')
