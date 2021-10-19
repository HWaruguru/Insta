from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post

@login_required(login_url='/accounts/login/')
def index(request):
    follows = ['peterthitu', 'gathu', 'kieya', 'alice', 'mary']
    posts = Post.objects.select_related().all()
    return render(request, "index.html", {"posts": posts, "follows": follows})
