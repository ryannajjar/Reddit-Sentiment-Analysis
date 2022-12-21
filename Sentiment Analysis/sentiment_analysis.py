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
    
    def title(self, post_relevance, num_posts):
        """Runs sentiment analysis on a specified amount of Reddit posts' titles under hot, new, top, or rising."""

        f = open('title_data.txt', 'w')

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            f.write(submission.title + '\n')
            f.write('\n')
            posttitle_doc = nlp(submission.title)
            f.write(f'The title of this post has a sentiment of: {posttitle_doc._.blob.polarity}\n')
            f.write(fm.mini_separator_1())

        f.close()

    def body(self, post_relevance, num_posts): # method is not complete, change after to include images after finishing class
        """Runs sentiment analysis on a specified amount of Reddit posts' body under hot, new, top, or rising."""

        f = open('body_data.txt', 'w')

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            f.write(fm.big_separator_1())
            f.write(fm.display_title(submission.title))
            f.write(fm.big_separator_1())

            f.write(submission.selftext + '\n')
            f.write('\n')
            postbody_doc = nlp(submission.selftext)
            f.write(f'The body of this post has a sentiment of: {postbody_doc._.blob.polarity}\n')
            f.write(fm.mini_separator_1())

        f.close()

    def top_comments(self, post_relevance, num_posts):
        """Runs sentiment analysis on the top comments of a reddit post, and averages the values to get a total idea of the sentiment."""

        f = open('comment_data.txt', 'w')

        for submission in eval(f'reddit.subreddit("{self.subreddit}").{post_relevance}(limit={num_posts})'):
            avg_sentiment = 0
            comments_analyzed = 0

            f.write(fm.big_separator_1())
            f.write(fm.display_title(submission.title))
            f.write(fm.big_separator_1())

            for top_level_comment in self._only_comments(submission.comments):
                if top_level_comment.body == '[deleted]':
                    f.write(top_level_comment.body + '\n')
                    f.write('UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS DELETED\n')
                    f.write(fm.mini_separator_2())
                elif top_level_comment.body == '[removed]':
                    f.write(top_level_comment.body + '\n')
                    f.write('UNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS REMOVED\n')
                    f.write(fm.mini_separator_2())
                else:
                    f.write(top_level_comment.body + '\n')
                    postcomment_doc = nlp(top_level_comment.body)
                    f.write(f'\n\nThis comment has a sentiment of: {postcomment_doc._.blob.polarity}\n')
                    avg_sentiment += postcomment_doc._.blob.polarity
                    comments_analyzed += 1
                    f.write(fm.mini_separator_2())

            if comments_analyzed == 0:
                f.write('There are no comments to analyze in this Reddit post.\n')
            else:
                avg_sentiment /= comments_analyzed
                f.write(fm.big_separator_2())
                f.write(fm.display_average_sentiment(avg_sentiment))

        f.close()
    
    def sub_comments(self, post_relevance, num_posts, level=2):
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
    
    def votes(self, post_relevance, num_posts):
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
    test = SubredditSA('chess')
    test.title('hot', 2)
    test.body('hot', 2)
    test.top_comments('hot', 2)
    test.sub_comments('hot', 2, 3)
    test.votes('hot', 2)
