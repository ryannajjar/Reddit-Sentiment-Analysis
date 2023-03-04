# Third-party
import praw

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# In-project
from config import nlp, reddit


def title(subreddit, post_relevance, num_posts=1):
    """Runs sentiment analysis on a specified amount of Reddit posts' titles under hot, new, top, or rising."""

    title_data = []

    for submission in eval(f'reddit.subreddit("{subreddit}").{post_relevance}(limit={num_posts})'):
        title_list = []

        posttitle_doc = nlp(submission.title)
        title_list.append((
            submission.title, 
            posttitle_doc._.blob.polarity
            ))

        title_data.append({
            'titles': title_list
        })
              
    return title_data
