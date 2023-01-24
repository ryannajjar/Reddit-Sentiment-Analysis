# In-project
import display_dat.methods.helper_methods.formatting as fm


# def display_votes_results(self, post_relevance, num_posts=1):
#     """Displays the data aquired from running the votes() method."""

#     f = open('votes_data.txt', 'w')
#     votes_data = self.votes(post_relevance, num_posts)

#     for data in votes_data:
#         f.write(fm.big_separator_1())
#         f.write(fm.display_title(data['title']))
#         f.write(fm.big_separator_1())

#         for vote in data['votes']:
#             f.write(fm.display_upvote_percentage(vote[0]))
#             f.write('\n')
#             f.write(fm.display_upvote_ratio_sentiment(vote[1]))
#             f.write(fm.mini_separator_1())

#     f.close()
