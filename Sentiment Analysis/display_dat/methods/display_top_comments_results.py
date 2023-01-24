# In-project
import display_dat.methods.helper_methods.formatting as fm


# def display_top_comments_results(self, post_relevance, num_posts=1):
#     """Displays the data aquired from running the top_comments() method."""

#     f = open('comment_data.txt', 'w')
#     top_comments_data = self.top_comments(post_relevance, num_posts)

#     for data in top_comments_data:
#         f.write(fm.big_separator_1())
#         f.write(fm.display_title(data['title']))
#         f.write(fm.big_separator_1())

#         for comment in data['comments']:
#             if comment[0] == '[deleted]':
#                 f.write(comment[0] + '\n')
#                 f.write(comment[1] + '\n')
#                 f.write(fm.mini_separator_2())
#             elif comment[0] == '[removed]':
#                 f.write(comment[0] + '\n')
#                 f.write(comment[1] + '\n')
#                 f.write(fm.mini_separator_2())
#             else:
#                 f.write(comment[0] + '\n')
#                 f.write(f'\n\nThis comment has a sentiment of: {comment[1]}\n')
#                 f.write(fm.mini_separator_2())
            
#         if data['average_sentiment'] == '':
#             f.write(comment[0])
#         else:
#             f.write(fm.big_separator_2())
#             f.write(fm.display_average_sentiment(data['average_sentiment']))
    
#     f.close()
