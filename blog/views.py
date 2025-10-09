from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import CommentForm
from .models import Post


def index(request):
    return render(request, "blog/index.html", {"posts": Post.objects.all()})


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(
        request,
        "blog/detail.html",
        {
            "post": post,
            "form": CommentForm(),
            "comments": post.comment_set.all(),
        },
    )


def comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            "blog/detail.html",
            {
                "post": post,
                "form": form,
                "comments": post.comment_set.all(),
            },
        )
    comment = form.save(commit=False)
    comment.post = post
    comment.save()
    return HttpResponseRedirect(reverse("blog:detail", args=(post_id,)))
