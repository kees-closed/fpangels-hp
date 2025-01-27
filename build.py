#!/usr/bin/python3

import json
import requests
import re
from dominate.tags import (
    link,
    script,
    meta,
    header,
    div,
    section,
    footer,
    h1,
    a,
    li,
    ul,
)
from dominate.util import raw
from dominate import document
from os import chown, chmod
from os.path import exists


chapters_data = "/var/lib/chapters_map/current_chapters.json"


# Get country code based on hashtag in group bio
def get_chapter_country(bio):
    hashtag = re.compile(r"\/tag\/(\w+)|#(\w+)")
    country = hashtag.search(bio)

    if country:
        for _hashtag in country.groups():
            if _hashtag:
                return _hashtag
    else:
        return "un"


# Get chapter JSON
if not exists(chapters_data):
    print("Local chapters data not found, fetching directly from Internet")
    response = requests.get("https://tzm.one/groups.json?filter=chapter")

    if response.status_code == requests.codes.ok:
        chapters = json.loads(response.text)["groups"]
else:
    with open(chapters_data, "r", encoding="utf8") as file:
        chapters = json.loads(file.read())

doc = document(title="TZM Chapters")
doc.set_attribute("lang", "en")

with doc.head:
    link(rel="stylesheet", href="style.min.css")
    link(rel="shortcut icon", href="resources/favicon.png")
    script(type="text/javascript", src="script.js")
    meta(name="viewport", content="width=device-width")
    meta(name="title", content="Chapters Map | The Zeitgeist Movement")
    meta(
        name="description",
        content="A global chapters overview of The Zeitgeist Movement",
    )
    meta(
        name="image",
        content="https://chapters.tzm.one/resources/seo-image.png",
    )
    meta(property="og:title", content="Chapters Map | The Zeitgeist Movement")
    meta(
        property="og:description",
        content="A global chapters overview of The Zeitgeist Movement",
    )
    meta(property="og:type", content="website")
    meta(property="og:url", content="https://chapters.tzm.one")
    meta(
        property="og:image",
        content="https://chapters.tzm.one/resources/seo-image.png",
    )

# Skeleton
header = doc.add(header()).add(div(cls="wrapper header"))
map = doc.add(div(cls="map"))
list = doc.add(section(cls="wrapper")).add(div(cls="annotated-list", id="chapters"))
footer = doc.add(footer()).add(div(cls="wrapper"))

# Header
header.add(h1("TZM Chapters"))
header.add(
    a(
        "More Info",
        href="https://tzm.one/quick-start",
        target="blank",
        cls="button btn-info",
    )
)

# Map
map.add(
    raw(
        """
        <iframe src="https://map.tzm.one/?show=chapters" allowfullscreen="true" frameborder="0"></iframe>
        """
    )
)

# List
list.add(
    raw(
        """
        <div class="menu">
          <input class="search" placeholder="Search">
          <button class="sort asc" data-sort="location">Sort by chapter</button>
          <button class="sort" data-sort="country">Sort by country</button>
        </div>
        """
    )
)
with list.add(div(cls="list")):
    for chapter in chapters:
        country = get_chapter_country(chapter["bio_excerpt"])
        title = chapter["title"]
        name = chapter["name"]
        member_count = chapter["user_count"]

        if "contact_by_email" in chapter["custom_fields"]:
            contact_by_email = chapter["custom_fields"]["contact_by_email"]
        else:
            contact_by_email = False
        if "show_map" in chapter["custom_fields"]:
            show_map = chapter["custom_fields"]["show_map"]
        else:
            show_map = False

        if show_map:
            with div(cls="chapter"):
                a(
                    "{c}".format(c=country.upper()),
                    href="https://tzm.one/tag/{c}".format(c=country),
                    target="blank",
                    cls="country",
                    data_location=title,
                )

                div(title, cls="location")

                if contact_by_email and member_count >= 1:
                    a(
                        "{n} member{s}".format(
                            n=member_count, s="s" if member_count > 1 else ""
                        ),
                        cls="button btn-chapters contact_via_email",
                        data_location=title,
                    )
                elif member_count >= 1:
                    a(
                        "{n} member{s}".format(
                            n=member_count, s="s" if member_count > 1 else ""
                        ),
                        href="https://tzm.one/groups/{name}".format(name=name),
                        target="blank",
                        cls="button btn-chapters",
                    )
                else:
                    a(
                        "No members",
                        href="https://tzm.one/groups/{name}".format(name=name),
                        target="blank",
                        cls="button btn-chapters",
                    )

list.add(
    raw(
        """
        <script src="list.js"></script>
        <script src="main.js"></script>
        """
    )
)

# Footer
with footer:
    with ul():
        li().add(
            a(
                "Contribute to this website on GitHub",
                href="https://github.com/kees-closed/fpangels-hp.git",
                target="blank",
            )
        )

with open("index.html", "w", encoding="utf8") as file:
    file.write(str(doc))
    try:
        chown("index.html", 33, 33)
    except OSError as e:
        print("Failed to change ownership: {}".format(e))
    chmod("index.html", 0o640)
