import praw
from creds import *

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob


reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)


nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')


class SubredditSA:
    """Runs sentiment analysis on a specified amount of Reddit posts under hot, new, top, or rising in a specific subreddit."""
    def __init__(self, subreddit):
        self.subreddit = subreddit
    
    def title(self, post_relevance, num_posts):
        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            print(submission.title)
            post_doc = nlp(submission.title)
            print(post_doc._.blob.polarity)
            print()

sa_test = SubredditSA('chess')
sa_test.title('hot', 10)
