# Third-party
from praw.models import MoreComments


def _only_comments(comments_obj):
    """Deals with errors relating to MoreComments, to yield only comments"""

    comments_obj.replace_more()
    for comment in comments_obj:
        if isinstance(comment, MoreComments):
            continue
        yield comment
        