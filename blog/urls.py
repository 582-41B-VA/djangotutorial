from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),
    path(
        "draft-comments/",
        views.draft_comments,
        name="draft_comments",
    ),
    path(
        "<int:post_id>/",
        views.detail,
        name="detail",
    ),
    path(
        "<int:post_id>/comment/create",
        views.create_comment,
        name="create_comment",
    ),
    path(
        "<int:post_id>/comment/draft/create",
        views.create_draft_comment,
        name="create_draft_comment",
    ),
]
