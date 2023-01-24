# In-project
import display_dat.methods.helper_methods.formatting as fm


# def display_sub_comments_results(self, post_relevance, num_posts=1, level=2):
#     """Displays the data aquired from running the sub_comments() method."""

#     f = open('comment_replies_data.txt', 'w')
#     sub_comments_data = self.sub_comments(post_relevance, num_posts, level)

#     for data in sub_comments_data:
#         f.write(fm.big_separator_1())
#         f.write(fm.display_title(data['title']))
#         f.write(fm.big_separator_1())

#         parents_counter = 0

#         for parent in data['parents']:
#             f.write('' if parents_counter == 0 else '\n')
#             f.write(parent['parent_content'] + '\n')
#             f.write('\n' if parent['replies'] else '')

#             parents_counter += 1

#             for reply in parent['replies']:
#                 if reply[0] == '[deleted]':
#                     f.write(fm.indent(reply[0]))
#                     f.write('\tUNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS DELETED\n')
#                     f.write(fm.mini_separator_2(True))
#                 elif reply[0] == '[removed]':
#                     f.write(fm.indent(reply[0]))
#                     f.write('\tUNABLE TO RUN SENTIMENT ANALYSIS, COMMENT WAS REMOVED\n')
#                     f.write(fm.mini_separator_2(True))
#                 else:
#                     f.write(fm.indent(reply[0]))
#                     f.write(f'\n\n\tThis comment reply has a sentiment of: {reply[1]}\n')
#                     f.write(fm.mini_separator_2(True))
#             f.write('\n' + fm.mini_separator_3())

#         if data['average_sentiment'] == '':
#             f.write(f'There are no sub comments in the Reddit post on level {level} to analyze.\n')
#         else:
#             f.write(fm.big_separator_2())
#             f.write(fm.display_average_sentiment(data['average_sentiment']))

#     f.close()
