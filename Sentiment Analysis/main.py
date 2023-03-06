# Third-party
import praw

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# In-project
import creds
import config

from data_collection.methods.title import title
from data_collection.methods.body import body
from data_collection.methods.top_comments import top_comments
from data_collection.methods.sub_comments import sub_comments
from data_collection.methods.votes import votes

from display_data.methods.display_title_results import display_title_results
from display_data.methods.display_body_results import display_body_results
from display_data.methods.display_top_comments_results import display_top_comments_results
from display_data.methods.display_sub_comments_results import display_sub_comments_results
from display_data.methods.display_votes_results import display_votes_results
