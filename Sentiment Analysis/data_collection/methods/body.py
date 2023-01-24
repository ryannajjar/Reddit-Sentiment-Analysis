# In-project
from data_collection.config import *


def body(subreddit, post_relevance, num_posts=1): # function is not complete, change after to include images after finishing class
    """Runs sentiment analysis on a specified amount of Reddit posts' body under hot, new, top, or rising."""
    
    body_data = []

    for submission in eval(f'reddit.subreddit("{subreddit}").{post_relevance}(limit={num_posts})'):
        body_list = []

        if submission.selftext == '' and submission.is_self is False:
            body_list.append((
                'THE POST DOES NOT HAVE ANY TEXT TO RUN SENTIMENT ANALYSIS ON',
                '',
                submission.url
            ))
        elif submission.selftext == '':
            body_list.append((
                'THE POST DOES NOT HAVE ANY TEXT TO RUN SENTIMENT ANALYSIS ON', 
                '',
                ''
                ))
        elif submission.selftext and submission.is_self is False:
            postbody_doc = nlp(submission.selftext)
            body_list.append((
                submission.selftext,
                postbody_doc._.blob.polarity,
                submission.url
            ))
        elif submission.selftext:
            postbody_doc = nlp(submission.selftext)
            body_list.append((
                submission.selftext, 
                postbody_doc._.blob.polarity,
                ''
                ))

        body_data.append({
            'title': submission.title,
            'content': body_list,
        })
    
    return body_data
    