# In-project
from data_collection.methods.helper_methods._upvote_ratio_to_sentiment_value import _upvote_ratio_to_sentiment_value


def votes(subreddit, post_relevance, num_posts=1):
    """Uses the ratio of upvotes to total votes to calculate the general sentiment."""

    votes_data = []

    for submission in eval(f'reddit.subreddit("{subreddit}").{post_relevance}(limit={num_posts})'):
        votes = []

        if post_relevance == 'new':
            if submission.score == 0 and submission.upvote_ratio == 0:
                votes.append((
                    submission.upvote_ratio * 100,
                    0.0
                ))

            elif 0 <= submission.score < 100 or submission.score < 0:
                votes.append((
                    submission.upvote_ratio * 100,
                    _upvote_ratio_to_sentiment_value(submission.upvote_ratio) / 3
                ))

            elif submission.score >= 100:
                votes.append((
                    submission.upvote_ratio * 100,
                    _upvote_ratio_to_sentiment_value(submission.upvote_ratio)
                ))

        else:
            votes.append((
                submission.upvote_ratio * 100,
                _upvote_ratio_to_sentiment_value(submission.upvote_ratio)
            ))

        votes_data.append({
            'title': submission.title,
            'votes': votes
        })
    
    return votes_data
