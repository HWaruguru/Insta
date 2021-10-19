from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Comment, Profile, Follow
from insta.forms import UpdateUserForm, UpdateUserProfileForm

@login_required(login_url='/accounts/login/')
def index(request):
    follows = ['peterthitu', 'gathu', 'kieya', 'alice', 'mary']
    posts = Post.objects.select_related().all()
    return render(request, "index.html", {"posts": posts, "follows": follows})

# @login_required(login_url='/accounts/login/')
# def profile(request):
#     follows = ['peterthitu', 'gathu', 'kieya', 'alice', 'mary']
#     posts = Post.objects.select_related().all()
#     return render(request, "profile.html", {"posts": posts, "follows": follows})

@login_required(login_url='login')
def profile(request):
    posts = request.user.profile.posts.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            print("\n\n\n\n")
            print(request.path_info)
            print("\n\n\n\n")
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form,
        'posts': posts,

    }
    return render(request, 'profile.html', params)


@login_required(login_url='login')
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    user_posts = user_prof.profile.posts.all()
    
    followers = Follow.objects.filter(followed=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    params = {
        'user_prof': user_prof,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'instagram/user_profile.html', params)

