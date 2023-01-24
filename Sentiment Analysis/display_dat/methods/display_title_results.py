# In-project
import display_dat.methods.helper_methods.formatting as fm
from data_collection import title


# def display_title_results(reddit, post_relevance, num_posts=1):
#     """Displays the data aquired from running the title() method."""

#     f = open('title_data.txt', 'w')
#     title_data = title(reddit, post_relevance, num_posts)

#     for data in title_data:
#         for title in data['titles']:
#             f.write(title[0] + '\n')
#             f.write('\n')
#             f.write(f'The title of this post has a sentiment of: {title[1]}\n')
#             f.write(fm.mini_separator_1())
        
#     f.close()
