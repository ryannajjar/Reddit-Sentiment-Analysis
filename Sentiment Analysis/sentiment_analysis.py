import praw
from creds import *

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob


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
    def __init__(self, subreddit):
        """Runs sentiment analysis on aspects of Reddit posts in a specific subreddit."""

        self.subreddit = subreddit
    
    def title(self, post_relevance, num_posts):
        """Runs sentiment analysis on a specified amount of Reddit posts' titles under hot, new, top, or rising."""

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            print(submission.title)
            print('\n' * 2)
            posttitle_doc = nlp(submission.title)
            print(f'The title of this post has a sentiment of: {posttitle_doc._.blob.polarity}')
            print('*' * 100 + '\n' * 2 + '*' * 100 + '\n')

    def body(self, post_relevance, num_posts): # method is not complete, change after to include images after finishing class
        """Runs sentiment analysis on a specified amount of Reddit posts' body under hot, new, top, or rising."""

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            print(f'Title of the post: {submission.title}')
            print('\n' * 2 + '[]' * 50 + '\n' * 2)
            print(submission.selftext)
            print('\n' * 2)
            postbody_doc = nlp(submission.selftext)
            print(f'The body of this post has a sentiment of: {postbody_doc._.blob.polarity}')
            print('*' * 100 + '\n' * 2 + '*' * 100 + '\n')

    def top_comments(self, post_relevance, num_posts):
        """Runs sentiment analysis on the top comments of a reddit post, and averages the values to get a total idea of the sentiment."""

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            avg_sentiment = 0
            comments_analyzed = 0

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
                    avg_sentiment += posttitle_doc._.blob.polarity
                    comments_analyzed += 1
                    print('\n' + '*' * 100 + '\n')

            if comments_analyzed == 0:
                print('There are no comments to analyze in this Reddit post.')
            else:
                avg_sentiment /= comments_analyzed
                print('\n' * 2 + '[]' * 50 + '\n' * 2)
                print(f'The sentiment of the people is: {avg_sentiment}')
                print('\n' * 2 + '[]' * 50 + '\n' * 2)
