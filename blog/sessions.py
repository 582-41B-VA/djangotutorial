from __future__ import annotations
from dataclasses import dataclass

from .models import Post


@dataclass
class DraftComment:
    """A draft comment saved by the user.

    Use __dict__ to convert to a dict when passing it to a Form instance.
    """

    name: str
    email: str
    body: str
    post: Post


class DraftCommentStore:
    """A store where draft comments for a session are saved."""

    _SESSION_ID = "draft_comments"

    def __init__(self, request):
        self.session = request.session
        _drafts = self.session.get(DraftCommentStore._SESSION_ID)
        if not _drafts:
            _drafts = self.session[DraftCommentStore._SESSION_ID] = {}
        self.drafts = _drafts

    def add(
        self, post_id: int, name: str, email: str, body: str
    ) -> DraftCommentStore:
        """Store a comment draft for the post with the given post_id."""
        # Session dict keys should be strings.
        # See: https://docs.djangoproject.com/en/5.2/topics/http/sessions/#session-object-guidelines
        self.drafts[str(post_id)] = {
            "name": name,
            "email": email,
            "body": body,
        }
        self._save()
        return self

    def delete(self, post_id) -> DraftCommentStore:
        """Delete the draft comment for the post with the given post_id."""
        del self.drafts[str(post_id)]
        self._save()
        return self

    def get(self, post_id: int) -> DraftComment | None:
        """Retrieve the comment draft for the post with the given post_id, if any."""
        draft = self.drafts.get(str(post_id))
        if not draft:
            return None
        post = Post.objects.get(pk=post_id)
        return DraftComment(draft["name"], draft["email"], draft["body"], post)

    def __len__(self) -> int:
        return len(self.drafts)

    def __iter__(self):
        for post_id, draft in self.drafts.items():
            post = Post.objects.get(pk=post_id)
            yield DraftComment(
                draft["name"], draft["email"], draft["body"], post
            )

    def _save(self):
        """Make sure to save the session.

        See: https://docs.djangoproject.com/en/5.2/topics/http/sessions/#when-sessions-are-saved
        """
        self.session.modified = True
