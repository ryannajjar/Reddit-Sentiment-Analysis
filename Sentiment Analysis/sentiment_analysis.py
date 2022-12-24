# Standard
from collections import deque

# In-project
import formatting as fm

# Third-party
import praw
from creds import *
from praw.models import MoreComments

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
    """Runs sentiment analysis on aspects of Reddit posts in a specific subreddit."""

    def __init__(self, subreddit):
        """Initializes the subreddit that data will be pulled from."""

        self.subreddit = subreddit
    
    def title(self, post_relevance, num_posts=1):
        """Runs sentiment analysis on a specified amount of Reddit posts' titles under hot, new, top, or rising."""

        title_data = []

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            posttitle_doc = nlp(submission.title)
            title_data.append((
                submission.title, 
                posttitle_doc._.blob.polarity
                ))
              
        return title_data

    def display_title_results(self, post_relevance, num_posts=1):
        """Displays the data aquired from running the title() method."""

        f = open('title_data.txt', 'w')
        title_data = self.title(post_relevance, num_posts)

        for data in title_data:
            f.write(data[0] + '\n')
            f.write('\n')
            f.write(f'The title of this post has a sentiment of: {data[1]}\n')
            f.write(fm.mini_separator_1())
            
        f.close()

    def body(self, post_relevance, num_posts=1): # method is not complete, change after to include images after finishing class
        """Runs sentiment analysis on a specified amount of Reddit posts' body under hot, new, top, or rising."""
        
        body_data = []

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            body_list = []

            if submission.selftext == '':
                body_list.append((
                    'THE POST DOES NOT HAVE ANY TEXT TO RUN SENTIMENT ANALYSIS ON', 
                    ''
                    ))
            else:
                postbody_doc = nlp(submission.selftext)
                body_list.append((
                    submission.selftext, 
                    postbody_doc._.blob.polarity
                    ))

            body_data.append({
                'title': submission.title,
                'body': body_list,
            })
        
        return body_data

    def display_body_results(self, post_relevance, num_posts=1):
        """Displays the data aquired from running the body() method."""

        f = open('body_data.txt', 'w')
        body_data = self.body(post_relevance, num_posts)

        for data in body_data:
            f.write('\n')
            f.write(fm.display_title(data['title']))
            f.write(fm.big_separator_1())

            for body in data['body']:
                if body[1] == '':
                    f.write(body[0] + '\n')
                    f.write('\n')
                    f.write(fm.mini_separator_1())
                else:
                    f.write(body[0] + '\n')
                    f.write('\n')
                    f.write(f'The body of this post has a sentiment of: {body[1]}\n')
                    f.write(fm.mini_separator_1())

        f.close()

    def top_comments(self, post_relevance, num_posts=1):
        """Runs sentiment analysis on the top comments of a reddit post, and averages the values to get a total idea of the sentiment."""

        top_comments_data = []

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            avg_sentiment = 0
            comment_list = []

            for top_level_comment in self._only_comments(submission.comments):  
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

    def display_top_comments_results(self, post_relevance, num_posts=1):
        """Displays the data aquired from running the top_comments() method."""

        f = open('comment_data.txt', 'w')
        top_comments_data = self.top_comments(post_relevance, num_posts)

        for data in top_comments_data:
            f.write(fm.big_separator_1())
            f.write(fm.display_title(data['title']))
            f.write(fm.big_separator_1())

            for comment in data['comments']:
                if comment[0] == '[deleted]':
                    f.write(comment[0] + '\n')
                    f.write(comment[1] + '\n')
                    f.write(fm.mini_separator_2())
                elif comment[0] == '[removed]':
                    f.write(comment[0] + '\n')
                    f.write(comment[1] + '\n')
                    f.write(fm.mini_separator_2())
                else:
                    f.write(comment[0] + '\n')
                    f.write(f'\n\nThis comment has a sentiment of: {comment[1]}\n')
                    f.write(fm.mini_separator_2())
                
            if data['average_sentiment'] == '':
                f.write(comment[0])
            else:
                f.write(fm.big_separator_2())
                f.write(fm.display_average_sentiment(data['average_sentiment']))
        
        f.close()

    def sub_comments(self, post_relevance, num_posts=1, level=2):
        """Runs sentiment analysis on the sub comments of a reddit post, and averages the values to get a total idea of the sentiment."""

        f = open('comment_replies_data.txt', 'w')
        
        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            avg_sentiment = 0
            comment_replies_analyzed = 0

            f.write(fm.big_separator_1())
            f.write(fm.display_title(submission.title))
            f.write(fm.big_separator_1())

            parents = []
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

                    if depth_counter == level - 1:
                        break

                parents += queue

            for parent_comment in parents:
                f.write('\n')
                f.write(parent_comment.body + '\n')
                f.write('\n')
                for comment_reply in self._only_comments(parent_comment.replies):
                    if comment_reply.body == '[deleted]':
                        f.write(fm.indent(comment_reply.body))
                        f.write('\tUNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS DELETED\n')
                        f.write(fm.mini_separator_2(True))
                    elif comment_reply.body == '[removed]':
                        f.write(fm.indent(comment_reply.body))
                        f.write('\tUNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS REMOVED\n')
                        f.write(fm.mini_separator_2(True))
                    else:
                        f.write(fm.indent(comment_reply.body))
                        postcommentreply_doc = nlp(comment_reply.body)
                        sentiment_value = postcommentreply_doc._.blob.polarity / 3
                        f.write(f'\n\n\tThis comment reply has a sentiment of: {sentiment_value}\n')
                        avg_sentiment += sentiment_value
                        comment_replies_analyzed += 1
                        f.write(fm.mini_separator_2(True))
                f.write(fm.mini_separator_3())

            if comment_replies_analyzed == 0:
                f.write(f'There are no sub comments in the Reddit post on level {level} to analyze.\n')
            else:
                avg_sentiment /= comment_replies_analyzed
                f.write(fm.big_separator_2())
                f.write(fm.display_average_sentiment(avg_sentiment))
            
        f.close()
    
    def votes(self, post_relevance, num_posts=1):
        """Uses the ratio of upvotes to total votes to calculate the general sentiment."""

        f = open('votes_data.txt', 'w')

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            f.write(fm.big_separator_1())
            f.write(fm.display_title(submission.title))
            f.write(fm.big_separator_1())

            if post_relevance == 'new':
                if submission.score == 0 and submission.upvote_ratio == 0:
                    f.write(fm.display_upvote_percentage(submission.upvote_ratio * 100))
                    f.write('\n')
                    f.write(fm.display_upvote_ratio_sentiment(0.0))
                    f.write(fm.mini_separator_1())
                elif 0 <= submission.score < 100 or submission.socre < 0:
                    f.write(fm.display_upvote_percentage(submission.upvote_ratio * 100))
                    f.write('\n')
                    f.write(fm.display_upvote_ratio_sentiment(self._upvote_ratio_to_sentiment_value(submission.upvote_ratio / 3)))
                    f.write(fm.mini_separator_1())
                elif submission.score >= 100:
                    f.write(fm.display_upvote_percentage(submission.upvote_ratio * 100))
                    f.write('\n')
                    f.write(fm.display_upvote_ratio_sentiment(self._upvote_ratio_to_sentiment_value(submission.upvote_ratio)))
                    f.write(fm.mini_separator_1())

            f.write(fm.display_upvote_percentage(submission.upvote_ratio * 100))
            f.write('\n')
            f.write(fm.display_upvote_ratio_sentiment(self._upvote_ratio_to_sentiment_value(submission.upvote_ratio)))
            f.write(fm.mini_separator_1())

        f.close()
    
    def _only_comments(self, comments_obj):
        """Deals with errors relating to MoreComments, to yield only comments"""

        comments_obj.replace_more()
        for comment in comments_obj:
            if isinstance(comment, MoreComments):
                continue
            yield comment
    
    def _upvote_ratio_to_sentiment_value(self, upvote_ratio):
        return 2 * upvote_ratio - 1


if __name__ == '__main__':
    pass
