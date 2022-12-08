import praw
from creds import *
from praw.models import MoreComments

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

from collections import deque


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
    def body(self, post_relevance, num_posts): # method is not complete, change after to include images after finishing class
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
                    postcomment_doc = nlp(top_level_comment.body)
                    print(f'This comment has a sentiment of: {postcomment_doc._.blob.polarity}')
                    avg_sentiment += postcomment_doc._.blob.polarity
                    comments_analyzed += 1
                    print('\n' + '*' * 100 + '\n')

            avg_sentiment /= comments_analyzed
            print('\n' * 2 + '[]' * 50 + '\n' * 2)
            print(f'The sentiment of the people is: {avg_sentiment}')
            print('\n' * 2 + '[]' * 50 + '\n' * 2)
    
    def sub_comments(self, post_relevance, num_posts, level=2):
        """Runs sentiment analysis on the sub comments of a reddit post, and averages the values to get a total idea of the sentiment."""
        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            avg_sentiment = 0
            comment_replies_analyzed = 0

            print(f'Title of the post: {submission.title}')
            print('\n' * 2 + '[]' * 50 + '\n' * 2)

            comment_replies_in_level = []
            for comment in self._only_comments(submission.comments):
                queue = deque([comment])
                visited = {comment}
                depth_counter = 1

                while len(queue) > 0:
                    for _ in range(len(queue)):
                        comment = queue.popleft()                            

                        for comment_reply in self._only_comments(comment.replies):
                            if comment_reply not in visited:
                                visited.add(comment_reply)
                                queue.append(comment_reply)

                    depth_counter += 1
                    if depth_counter == level:
                        break

                comment_replies_in_level += queue
                    
            # Process comment replies in desired level
            for comment_reply in comment_replies_in_level:
                print(comment_reply.body)
                postcommentreply_doc = nlp(comment_reply.body)
                sentiment_value = postcommentreply_doc._.blob.polarity / 3
                print(f'This comment reply has a sentiment of: {sentiment_value}')
                avg_sentiment += sentiment_value
                comment_replies_analyzed += 1
                print('\n' + '*' * 100 + '\n')

            if comment_replies_analyzed == 0:
                print(f'There are no sub comments in the Reddit post on level {level} to analyze.')
            else:
                avg_sentiment /= comment_replies_analyzed
                print('\n' * 2 + '[]' * 50 + '\n' * 2)
                print(f'The sentiment of the people is: {avg_sentiment}')
                print('\n' * 2 + '[]' * 50 + '\n' * 2)
    
    def _only_comments(self, comments_obj):
        """Deals with errors relating to MoreComments, to yield only comments"""
        comments_obj.replace_more()
        for comment in comments_obj:
            if isinstance(comment, MoreComments):
                continue
            yield comment


test = SubredditSA('chess')
test.sub_comments('hot', 10, 3)
