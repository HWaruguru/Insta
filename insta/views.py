from django.shortcuts import render
from .models import Post


def index(request):
    follows = ['peterthitu', 'gathu', 'kieya', 'alice', 'mary']
    posts = Post.objects.select_related().all()
    return render(request, "index.html", {"posts": posts, "follows": follows})
