# In-project
import display_data.methods.helper_methods.formatting as fm


def display_body_results(collected_data, type, append=False):
    """Displays the data aquired from running the body() method."""

    if type == 'txt':
        t = open('display_data/methods/templates/body_templates/body_display_template.txt', 'r')
        d = open('body_data.txt', 'a')
    elif type == 'md':
        t = open('display_data/methods/templates/body_templates/body_display_template.md', 'r')
        d = open('body_data.md', 'a')
    elif type == 'raw':
        f = open('body_data.txt', 'w')
        f.write(str(collected_data))
        f.close()
        return
    
    if not append:
        d.truncate(0)

    for data in collected_data:
        t.seek(0)
        template = t.read()
        template = template.replace('{title}', data['title'])

        for body_info in data['content']:
            if body_info[1] == '' and body_info[2] == '':
                template = template.replace('{body}', body_info[0])
                template = template.replace('{url}', '')
                template = template.replace('{sentiment}', '')
            elif body_info[1] == '':
                template = template.replace('{body}', body_info[0])
                template = template.replace('{url}', f'{fm.mini_separator_2()}\nUrl that the Reddit post links to: {body_info[2]}')
                template = template.replace('{sentiment}', '')
            elif body_info[1] != '' and body_info[2] != '':
                template = template.replace('{body}', body_info[0])
                template = template.replace('{url}', f'{fm.mini_separator_2()}\nUrl that the Reddit post links to: {body_info[2]}{fm.mini_separator_2()}')
                template = template.replace('{sentiment}', f'The body of this post has a sentiment of: {body_info[1]}')
            elif body_info[1] != '':
                template = template.replace('{body}', body_info[0])
                template = template.replace('{url}', '')
                template = template.replace('{sentiment}', f'The body of this post has a sentiment of: {body_info[1]}')

            d.write(template)

    t.close()
    d.close()
