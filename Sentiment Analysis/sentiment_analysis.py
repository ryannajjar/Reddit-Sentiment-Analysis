import praw
from creds import *

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

import requests


reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD
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
            print('*' * 100 + '\n' * 2 + '*' * 100 + '\n')

    """Runs sentiment analysis on a specified amount of Reddit posts' body under hot, new, top, or rising."""
    def body(self, post_relevance, num_posts): # method is not complete, fix so that it includes images
        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            print(f'Title of the post: {submission.title}')
            print('\n' * 2 + '[]' * 50 + '\n' * 2)
            print(submission.selftext)
            print('\n' * 2)
            postbody_doc = nlp(submission.selftext)
            print(f'The body of this post has a sentiment of: {postbody_doc._.blob.polarity}')
            print('*' * 100 + '\n' * 2 + '*' * 100 + '\n')

    """Runs sentiment analysis on the top comments of a reddit post, and averages the values to get a total idea of the sentiment."""
    def top_comments(self, post_relevance, num_posts):
        sentiment_values = []
        total_sentiment = 0

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            print(f'Title of the post: {submission.title}')
            print('\n' * 2 + '[]' * 50 + '\n' * 2)
            for top_level_comment in submission.comments:
                if top_level_comment.body == '[deleted]':
                    print(top_level_comment.body)
                    print('UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS DELETED')
                    print('\n' + '*' * 100 + '\n')
                elif top_level_comment.body == '[removed]':
                    print(top_level_comment.body)
                    print('UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS REMOVED')
                    print('\n' + '*' * 100 + '\n')
                else:
                    print(top_level_comment.body)
                    posttitle_doc = nlp(top_level_comment.body)
                    print(f'This comment has a sentiment of: {posttitle_doc._.blob.polarity}')
                    sentiment_values.append(posttitle_doc._.blob.polarity)
                    print('\n' + '*' * 100 + '\n')

            for sentiment in sentiment_values:
                total_sentiment += sentiment
            total_sentiment /= len(sentiment_values)
            print('\n' * 2 + '[]' * 50 + '\n' * 2)
            print(f'The sentiment of the people is: {total_sentiment}')
            print('\n' * 2 + '[]' * 50 + '\n' * 2)


test = SubredditSA('chess')
test.top_comments('hot', 2)
