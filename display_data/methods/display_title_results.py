# In-project
import display_data.methods.helper_methods.formatting as fm


def display_title_results(collected_data, type, append=False):
    """Displays the data aquired from running the title() method."""

    if type == 'txt':
        t = open('display_data/methods/templates/title_templates/title_display_template.txt', 'r')
        d = open('title_data.txt', 'a')
    elif type == 'md':
        t = open('display_data/methods/templates/title_templates/title_display_template.md', 'r')
        d = open('title_data.md', 'a')
    elif type == 'raw':
        f = open('title_data.txt', 'w')
        f.write(str(collected_data))
        f.close()
        return

    if not append:
        d.truncate(0)
    
    for data in collected_data:
        t.seek(0)
        template = t.read()
        for title in data['titles']:
            template = template.replace('{title}', title[0])
            template = template.replace('{sentiment}', str(title[1]))

            d.write(template)
    
    t.close()
    d.close()
