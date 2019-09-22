
def prepare_link(link):
    print(link)
    splitted_link = str(link).split('=')
    print(splitted_link)
    link = splitted_link[2] if len(splitted_link) > 2 else ''
    markdown_message = '[Watch here](' + str(link) + ')'
    return markdown_message


def prepare_pretty_data(data):
    print(data)
    if data["Response"] == "False":
        return '*' + data["Error"] + '*'
    template = 'Title:\n*' + data['Title'] + '*\nYear: ' \
               + data['Year'] + '\nGenre: ' + data['Genre'] + \
               data['Genre'] + '\nDirector: ' + data['Director'] + \
               '\nPlot: ' + data['Plot'] + '\nRating: ' + \
               data['Ratings'][0]["Value"] + \
               '\n[Poster](' + data["Poster"] + ')'

    return template
