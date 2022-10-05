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
    """Runs sentiment analysis on aspects of Reddit posts in a specific subreddit."""
    def __init__(self, subreddit):
        self.subreddit = subreddit
    
    """Runs sentiment analysis on a specified amount of Reddit posts' titles under hot, new, top, or rising."""
    def title(self, post_relevance, num_posts):
        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            print(submission.title)
            print('\n' * 2)
            posttitle_doc = nlp(submission.title)
            print(f'The title of this post has a sentiment of: {posttitle_doc._.blob.polarity}')
            print('*' * 100 + '\n' * 2 + '*' * 100)

    """Runs sentiment analysis on a specified amount of Reddit posts' body under hot, new, top, or rising."""
    def body(self, post_relevance, num_posts): # method is not complete, fix so that it includes images
        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            print(submission.selftext)
            print('\n' * 2)
            postbody_doc = nlp(submission.selftext)
            print(f'The body of this post has a sentiment of: {postbody_doc._.blob.polarity}')
            print('*' * 100 + '\n' * 2 + '*' * 100)

test = SubredditSA('chess')
test.body('hot', 7)