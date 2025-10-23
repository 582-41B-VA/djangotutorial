from .sessions import DraftCommentStore


def draft_comments(request):
    return {"draft_comments": DraftCommentStore(request)}
