# In-project
import display_data.methods.helper_methods.formatting as fm


def display_top_comments_results(collected_data, type, append=False):
    """Displays the data aquired from running the top_comments() method."""

    # check the type of file the user requested and open the appropriate files
    if type == 'txt':
        t = open('display_data/methods/templates/top_comments_templates/top_comments_display_template.txt', 'r')
        d = open('comment_data.txt', 'a')
    elif type == 'md':
        t = open('display_data/methods/templates/top_comments_templates/top_comments_display_template.md', 'r')
        d = open('comment_data.md', 'a')
        md = True
    elif type == 'raw':
        f = open('comment_data.txt', 'w')
        f.write(str(collected_data))
        f.close()
        return
    
    # reset the displaying file if append is still set to False
    if not append:
        d.truncate(0)

    for data in collected_data:
        t.seek(0)
        template = t.read()
        template = template.replace('{title}', data['title'])

        for comment in data['comments']:
            if comment[0] == '[deleted]':
                template = template.replace('{comment}', comment[0])
                template = template.replace('{sentiment}', comment[1] 
                                            + fm.mini_separator_2(False, md) + 
                                            ('\n## {comment}\n\n\n### {sentiment}' if md else '\n{comment}\n\n\n{sentiment}'))
            elif comment[0] == '[removed]':
                template = template.replace('{comment}', comment[0])
                template = template.replace('{sentiment}', comment[1] 
                                            + fm.mini_separator_2(False, md) + 
                                            ('\n## {comment}\n\n\n### {sentiment}' if md else '\n{comment}\n\n\n{sentiment}'))
            else:
                template = template.replace('{comment}', comment[0])
                template = template.replace('{sentiment}', f'This comment has a sentiment of: {str(comment[1])}'
                                            + fm.mini_separator_2(False, md) + 
                                            ('\n## {comment}\n\n\n### {sentiment}' if md else '\n{comment}\n\n\n{sentiment}'))
                
        template = template.replace(('\n## {comment}\n\n\n### {sentiment}' if md else '\n{comment}\n\n\n{sentiment}'), '')
            
        if data['average_sentiment'] == '':
            template = template.replace('{comment}', comment[0])
        else:
            template = template.replace('{avg_sentiment}', f"The sentiment of the people is: {str(data['average_sentiment'])}")
        
        d.write(template)
    
    t.close()
    d.close()
