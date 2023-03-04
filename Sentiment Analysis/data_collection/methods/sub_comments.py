# Standard
from collections import deque

# Third-party
import praw

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# In-project
from config import nlp, reddit

from data_collection.methods.helper_methods._only_comments import _only_comments


def sub_comments(subreddit, post_relevance, num_posts=1, level=2):
    """Runs sentiment analysis on the sub comments of a reddit post, and averages the values to get a total idea of the sentiment."""

    sub_comments_data = []
    
    for submission in eval(f'reddit.subreddit("{subreddit}").{post_relevance}(limit={num_posts})'):
        parents = []
        for comment in _only_comments(submission.comments):
            queue = deque([comment])
            visited = {comment}
            depth_counter = 1

            while len(queue) > 0:
                for _ in range(len(queue)):
                    comment = queue.popleft()                            

                    for comment_reply in _only_comments(comment.replies):
                        if comment_reply not in visited:
                            visited.add(comment_reply)
                            queue.append(comment_reply)

                depth_counter += 1

                if depth_counter == level - 1:
                    break

            parents += queue

        avg_sentiment = 0
        comment_replies_analyzed = 0
        parents_list = []

        for parent_comment in parents:
            replies_list = []

            for comment_reply in _only_comments(parent_comment.replies):
                if comment_reply.body in ['[deleted]', '[removed]']:
                    sentiment = f'UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS {comment_reply.body[1:-1].upper()}'
                else:
                    postcommentreply_doc = nlp(comment_reply.body)
                    sentiment = postcommentreply_doc._.blob.polarity / level
                    avg_sentiment += sentiment

                comment_replies_analyzed += 1

                replies_list.append((
                    comment_reply.body,
                    sentiment
                ))

            parents_list.append({
                'parent_content': parent_comment.body,
                'replies': replies_list
            })

        if comment_replies_analyzed == 0:
            avg_sentiment = ''
        else:
            avg_sentiment /= comment_replies_analyzed
            
        sub_comments_data.append({
            'title': submission.title,
            'level': level,
            'parents': parents_list,
            'average_sentiment': avg_sentiment
        })

    return sub_comments_data
