# In-project
import display_data.methods.helper_methods.formatting as fm


def display_body_results(collected_data):
    """Displays the data aquired from running the body() method."""

    f = open('body_data.txt', 'w')
    body_data = collected_data

    for data in body_data:
        f.write('\n')
        f.write(fm.display_title(data['title']))
        f.write(fm.big_separator_1())

        for body_info in data['content']:
            if body_info[1] == '' and body_info[2] == '':
                f.write(body_info[0] + '\n')
                f.write('\n')
                f.write(fm.mini_separator_1())
            elif body_info[1] == '':
                f.write(body_info[0] + '\n')
                f.write('\n')
                f.write(fm.mini_separator_2())
                f.write(f'Url that the Reddit post links to: {body_info[2]}')
                f.write(fm.mini_separator_1())
            elif body_info[1] and body_info[2]:
                f.write(body_info[0] + '\n')
                f.write('\n')
                f.write(fm.mini_separator_2())
                f.write(f'Url that the Reddit post links to: {body_info[2]}')
                f.write(fm.mini_separator_2())
                f.write('\n')
                f.write(f'The body of this post has a sentiment of: {body_info[1]}\n')
                f.write(fm.mini_separator_1())
            elif body_info[1]:
                f.write(body_info[0] + '\n')
                f.write('\n')
                f.write(f'The body of this post has a sentiment of: {body_info[1]}\n')
                f.write(fm.mini_separator_1())

    f.close()
