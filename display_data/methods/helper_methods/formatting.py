def display_title(title):
    return f'Title of the post: {title}\n'

def big_separator_1():
    return '\n' + '[]' * 50 + '\n' * 2

def big_separator_2():
    return '\n' * 2 + '[]' * 50 + '\n' * 2

def mini_separator_1():
    return '*' * 100 + '\n' * 2 + '*' * 100 + '\n'

def mini_separator_2(ind=False, md=False):
    return '\n' + ('\t' if ind else '') + ('<hr>' if md else '*' * 100) + '\n'

def mini_separator_3():
    return '*' * 100 + '\n'

def indent(text):
    return '\t' + text.replace('\n', '\n\t').rstrip('\t') + '\n'

def display_average_sentiment(avg_sentiment_value):
    return f'The sentiment of the people is: {avg_sentiment_value}\n'

def display_upvote_percentage(upvote_ratio):
    return f'{upvote_ratio}% of the votes on this post are upvotes.\n'

def display_upvote_ratio_sentiment(sentiment_value):
    return f'Based on upvote ratio, the sentiment of the people is: {sentiment_value}\n'
