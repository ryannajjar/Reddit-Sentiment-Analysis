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
    def __init__(self, subreddit):
        """Runs sentiment analysis on aspects of Reddit posts in a specific subreddit."""

        self.subreddit = subreddit
    
    def title(self, post_relevance, num_posts):
        """Runs sentiment analysis on a specified amount of Reddit posts' titles under hot, new, top, or rising."""

        f = open('title_data.txt', 'w')

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            f.write(submission.title + '\n')
            f.write('\n')
            posttitle_doc = nlp(submission.title)
            f.write(f'The title of this post has a sentiment of: {posttitle_doc._.blob.polarity}\n')
            f.write('*' * 100 + '\n' * 2 + '*' * 100 + '\n')

        f.close()

    def body(self, post_relevance, num_posts): # method is not complete, change after to include images after finishing class
        """Runs sentiment analysis on a specified amount of Reddit posts' body under hot, new, top, or rising."""

        f = open('body_data.txt', 'w')

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            f.write('\n' + '[]' * 50 + '\n' * 2)
            f.write(f'Title of the post: {submission.title}\n')
            f.write('\n' + '[]' * 50 + '\n' * 2)

            f.write(submission.selftext + '\n')
            f.write('\n')
            postbody_doc = nlp(submission.selftext)
            f.write(f'The body of this post has a sentiment of: {postbody_doc._.blob.polarity}\n')
            f.write('*' * 100 + '\n' * 2 + '*' * 100 + '\n')

        f.close()

    def top_comments(self, post_relevance, num_posts):
        """Runs sentiment analysis on the top comments of a reddit post, and averages the values to get a total idea of the sentiment."""

        f = open('comment_data.txt', 'w')

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            avg_sentiment = 0
            comments_analyzed = 0

            f.write('\n' + '[]' * 50 + '\n' * 2)
            f.write(f'Title of the post: {submission.title}\n')
            f.write('\n' + '[]' * 50 + '\n' * 2)

            for top_level_comment in self._only_comments(submission.comments):
                if top_level_comment.body == '[deleted]':
                    f.write(top_level_comment.body + '\n')
                    f.write('UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS DELETED\n')
                    f.write('\n' + '*' * 100 + '\n')
                elif top_level_comment.body == '[removed]':
                    f.write(top_level_comment.body + '\n')
                    f.write('UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS REMOVED\n')
                    f.write('\n' + '*' * 100 + '\n')
                else:
                    f.write(top_level_comment.body + '\n')
                    postcomment_doc = nlp(top_level_comment.body)
                    f.write(f'\n\nThis comment has a sentiment of: {postcomment_doc._.blob.polarity}\n')
                    avg_sentiment += postcomment_doc._.blob.polarity
                    comments_analyzed += 1
                    f.write('\n' + '*' * 100 + '\n')

            if comments_analyzed == 0:
                f.write('There are no comments to analyze in this Reddit post.\n')
            else:
                avg_sentiment /= comments_analyzed
                f.write('\n' * 2 + '[]' * 50 + '\n' * 2)
                f.write(f'The sentiment of the people is: {avg_sentiment}\n')

        f.close()
    
    def sub_comments(self, post_relevance, num_posts, level=2):
        """Runs sentiment analysis on the sub comments of a reddit post, and averages the values to get a total idea of the sentiment."""

        f = open('comment_replies_data.txt', 'w')
        
        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            avg_sentiment = 0
            comment_replies_analyzed = 0

            f.write('\n' + '[]' * 50 + '\n' * 2)
            f.write(f'Title of the post: {submission.title}\n')
            f.write('\n' + '[]' * 50 + '\n' * 2)

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
                if comment_reply.body == '[deleted]':
                    f.write(comment_reply.body + '\n')
                    f.write('UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS DELETED\n')
                    f.write('\n' + '*' * 100 + '\n')
                elif comment_reply.body == '[removed]':
                    f.write(comment_reply.body + '\n')
                    f.write('UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS REMOVED\n')
                    f.write('\n' + '*' * 100 + '\n')
                else:
                    f.write(comment_reply.body + '\n')
                    postcommentreply_doc = nlp(comment_reply.body)
                    sentiment_value = postcommentreply_doc._.blob.polarity / 3
                    f.write(f'\n\nThis comment reply has a sentiment of: {sentiment_value}\n')
                    avg_sentiment += sentiment_value
                    comment_replies_analyzed += 1
                    f.write('\n' + '*' * 100 + '\n')

            if comment_replies_analyzed == 0:
                f.write(f'There are no sub comments in the Reddit post on level {level} to analyze.\n')
            else:
                avg_sentiment /= comment_replies_analyzed
                f.write('\n' * 2 + '[]' * 50 + '\n' * 2)
                f.write(f'The sentiment of the people is: {avg_sentiment}\n')
            
        f.close()
    
    def votes(self, post_relevance, num_posts):
        """Uses the ratio of upvotes to total votes to calculate the general sentiment."""

        f = open('votes_data.txt', 'w')

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            f.write('\n' + '[]' * 50 + '\n' * 2)
            f.write(f'Title of the post: {submission.title}\n')
            f.write('\n' + '[]' * 50 + '\n' * 2)
    
    def _only_comments(self, comments_obj):
        """Deals with errors relating to MoreComments, to yield only comments"""

        comments_obj.replace_more()
        for comment in comments_obj:
            if isinstance(comment, MoreComments):
                continue
            yield comment


if __name__ == '__main__':
    pass
