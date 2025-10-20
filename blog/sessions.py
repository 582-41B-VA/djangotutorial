from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DraftComment:
    """A draft comment saved by the user.

    Use __dict__ to convert to a dict when passing it to a Form instance.
    """

    name: str
    email: str
    body: str


class DraftCommentStore:
    """A store where draft comments for a session are saved."""

    _SESSION_ID = "draft_comments"

    def __init__(self, request):
        self.session = request.session
        drafts = self.session.get(DraftCommentStore._SESSION_ID)
        if not drafts:
            drafts = self.session[DraftCommentStore._SESSION_ID] = {}
        self.drafts = drafts

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
        return DraftComment(draft["name"], draft["email"], draft["body"])

    def _save(self):
        """Make sure to save the session.

        See: https://docs.djangoproject.com/en/5.2/topics/http/sessions/#when-sessions-are-saved
        """
        self.session.modified = True
