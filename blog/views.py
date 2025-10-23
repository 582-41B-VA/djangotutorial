from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages

from .forms import CommentForm
from .models import Post
from .sessions import DraftCommentStore


def index(request):
    return render(request, "blog/index.html", {"posts": Post.objects.all()})


def draft_comments(request):
    return render(request, "blog/draft_comments.html")


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    draft_comment = DraftCommentStore(request).get(post_id)
    return render(
        request,
        "blog/detail.html",
        {
            "post": post,
            "form": CommentForm(
                draft_comment.__dict__ if draft_comment else None
            ),
            "comments": post.comment_set.all(),
        },
    )


def create_comment(request, post_id):
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

    drafts = DraftCommentStore(request)
    drafts.delete(post_id)

    return HttpResponseRedirect(reverse("blog:detail", args=(post_id,)))


def create_draft_comment(request, post_id):
    drafts = DraftCommentStore(request)
    drafts.add(
        post_id,
        request.POST["name"],
        request.POST["email"],
        request.POST["body"],
    )
    messages.success(request, "Your draft was saved.")
    return HttpResponseRedirect(reverse("blog:detail", args=(post_id,)))
