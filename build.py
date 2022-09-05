import dominate, json, os.path, requests, yaml
import re
from dominate.tags import *
from dominate.util import raw

# Get chapter JSON
response = requests.get('https://forum.tzm.community/groups.json?filter=chapter')

def get_chapter_country(bio):
    hashtag = re.compile('#(\w+)')
    country = (hashtag.search(bio))

    if country:
        return country.group(1)
    else:
        return 'un'

if response.status_code == requests.codes.ok:
    chapters = json.loads(response.text)['groups']
    doc = dominate.document(title='TZM Chapters')

    with doc.head:
        link(rel='stylesheet', href='style.css')
        link(rel='stylesheet', href='https://emoji-css.afeld.me/emoji.css')
        link(rel='shortcut icon', href='resources/favicon.png')
        script(type='text/javascript', src='script.js')
        meta(name='viewport', content='width=device-width')

    # Skeleton
    header = doc.add(header()).add(div(cls='wrapper'))
    map = doc.add(div(cls='map'))
    list = doc.add(section(cls='wrapper')).add(div(cls='annotated-list', id='chapters'))
    footer = doc.add(footer()).add(div(cls='wrapper'))

    # Header
    header.add(h1('TZM Chapters'))
    header.add(a('More Info', cls='button btn-info', href='https://forum.tzm.community/about-tzm', target='blank'))

    # Map
    map.add(raw("""
        <iframe src="https://map.tzm.community/?show=chapters" allowfullscreen="true" frameborder="0">
            <p><a href="https://map.tzm.community/?show=chapters" target="_blank">See the TZM Chapters Map!</a></p>
        </iframe>
        """))

    # List
    list.add(raw("""
        <input class="search" placeholder="Search">
        <button class="sort asc" data-sort="location">Sort by chapter</button>
        <button class="sort" data-sort="country">Sort by country</button>"""))
    with list.add(div(cls='list')):
        for chapter in chapters:
            country = get_chapter_country(chapter['bio_excerpt'])
            title = chapter['title']
            name = chapter['name']
            member_count = chapter['user_count']

            if 'contact_chapter_by_email' in chapter['custom_fields']:
                contact_by_email = chapter['custom_fields']['contact_chapter_by_email']
            else:
                contact_by_email = False
            if 'show_map' in chapter['custom_fields']:
                show_map = chapter['custom_fields']['show_map']
            else:
                show_map = False

            if member_count > 0 and show_map:
                with div(cls='chapter'):
                  div(raw('<i class="em em-flag-{country}"></i>'.format(country=country)), cls='country')
                  #div(country, cls='em em-flag-{country}'.format(country=country)) # TODO: sorting doesn't work when the class is not unique
                  div(title, cls='location')

                  if contact_by_email:
                      a('Contact {n} member{s} via mail'.format(n=member_count, s='s' if member_count > 1 else ''),
                        cls='button btn-chapters contact_via_email', data_location=title)
                  else:
                      a('Contact {n} member{s} via forum'.format(n=member_count, s='s' if member_count > 1 else ''),
                        href='https://forum.tzm.community/groups/{name}'.format(name=name), target='blank', cls='button btn-chapters')

    list.add(raw("""
        <script src="list.js"></script>
        <script src="main.js"></script>"""))

    # Footer
    with footer:
        with ul():
            li().add(a('Contribute to this website on GitHub', href='https://github.com/kees-closed/fpangels-hp.git', target='blank'))


    with open('index.html', 'w', encoding='utf8') as file:
        file.write(str(doc))
