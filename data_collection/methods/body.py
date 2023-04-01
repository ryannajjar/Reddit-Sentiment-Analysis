# Third-party
import praw

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# In-project
from config import nlp, reddit


def body(subreddit, post_relevance, num_posts=1): # function is not complete, change after to include images after finishing class
    """Runs sentiment analysis on a specified amount of Reddit posts' body under hot, new, top, or rising."""
    
    body_data = []

    for submission in eval(f'reddit.subreddit("{subreddit}").{post_relevance}(limit={num_posts})'):
        body_list = []

        # for posts without text that link to something else
        if submission.selftext == '' and submission.is_self is False:
            body_list.append((
                'THE POST DOES NOT HAVE ANY TEXT TO RUN SENTIMENT ANALYSIS ON',
                '',
                submission.url
            ))
        # for posts without text that do not link to something else
        elif submission.selftext == '':
            body_list.append((
                'THE POST DOES NOT HAVE ANY TEXT TO RUN SENTIMENT ANALYSIS ON', 
                '',
                ''
                ))
        # for posts with text that link to something else
        elif submission.selftext and submission.is_self is False:
            postbody_doc = nlp(submission.selftext)
            body_list.append((
                submission.selftext,
                postbody_doc._.blob.polarity,
                submission.url
            ))
        # for posts with text that do not link to something else
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
