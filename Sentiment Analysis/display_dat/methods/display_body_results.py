# In-project
import display_dat.methods.helper_methods.formatting as fm


# def display_body_results(self, post_relevance, num_posts=1):
#     """Displays the data aquired from running the body() method."""

#     f = open('body_data.txt', 'w')
#     body_data = self.body(post_relevance, num_posts)

#     for data in body_data:
#         f.write('\n')
#         f.write(fm.display_title(data['title']))
#         f.write(fm.big_separator_1())

#         for body in data['body']:
#             if body[1] == '' and body[2] == '':
#                 f.write(body[0] + '\n')
#                 f.write('\n')
#                 f.write(fm.mini_separator_1())
#             elif body[1] == '':
#                 f.write(body[0] + '\n')
#                 f.write('\n')
#                 f.write(fm.mini_separator_2())
#                 f.write(f'Url that the Reddit post links to: {body[2]}')
#                 f.write(fm.mini_separator_1())
#             elif body[1]:
#                 f.write(body[0] + '\n')
#                 f.write('\n')
#                 f.write(f'The body of this post has a sentiment of: {body[1]}\n')
#                 f.write(fm.mini_separator_1())

#     f.close()
