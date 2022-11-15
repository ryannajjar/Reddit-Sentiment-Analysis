# **Reddit API Project Collection**

## This is a repository of projects that use the PRAW Reddit API.

### <u> Project #1: "Sentiment Analysis" </u>

<br>

Sentiment analysis is when a program analyzes something, usually text, to determine the charge of the conotation of that thing, i.e. how positive or negative it is.

<br>

This project uses the Spacy library to run sentiment analysis on different aspects of a Reddit post, and then caclulates the total sentiment of the post and what people think about the post using the sentiment values from those aspects.

<br>

There is a `SubredditSA` class that has six methods:

1. `title`: The `title` method analyzes the title of a specified number of Reddit posts within a subreddit, and outputs their sentiment values.

2. `body`: The `body` method analyzes the content of a specified number of Reddit posts within a subreddit, and outputs their sentiment values.

3. `top_comments`: The `top_comments` method analyzes all the top comments of a specified number of Reddit posts within a subreddit, and outputs the sentiment values of the individual comments, as well as the avergae sentiment value of all the comments combined.

4. `sub_comments`: The `sub_comments` method analyzes a specified number of sub comments of a specified number of Reddit posts within a subreddit, and outputs the sentiment values of the individual comments, as well as the average sentiment value of all the comments combined.

5. `votes`: The `votes` method compares the ratio of upvotes to downvotes on a specified number of Reddit posts within a subreddit, and outputs the sentiment values of the posts based on that ratio.

6. `_multi_analysis`: The `_multi_analysis` semi-private method combines two or more of the previously mentioned methods to calculate a total sentiment value that is more accurate.
