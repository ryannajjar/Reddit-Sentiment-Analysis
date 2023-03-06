# Third-party
import praw

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# In-project
from config import nlp, reddit

from data_collection.methods.helper_methods._only_comments import _only_comments


def top_comments(subreddit, post_relevance, num_posts=1):
    """Runs sentiment analysis on the top comments of a reddit post, and averages the values to get a total idea of the sentiment."""

    top_comments_data = []

    for submission in eval(f'reddit.subreddit("{subreddit}").{post_relevance}(limit={num_posts})'):
        avg_sentiment = 0
        comment_list = []

        for top_level_comment in _only_comments(submission.comments):  
            if top_level_comment.body in ['[deleted]', '[removed]']:
                sentiment = f'UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS {top_level_comment.body[1:-1].upper()}'
            else:
                postcomment_doc = nlp(top_level_comment.body)
                sentiment = postcomment_doc._.blob.polarity
                avg_sentiment += sentiment
            
            comment_list.append((
                top_level_comment.body,
                sentiment
            ))

        if len(comment_list) == 0:
            comment_list.append((
                'There are no comments to analyze in this Reddit post.',
                ''
            ))

            avg_sentiment = ''
        else:
            avg_sentiment /= len(comment_list)

        top_comments_data.append({
            'title': submission.title,
            'comments': comment_list,
            'average_sentiment': avg_sentiment
        })
    
    return top_comments_data
