from bs4 import BeautifulSoup
import requests

def add_score(a_dict, a_dict_tup, score, count):
    name = a_dict_tup[count][0]
    a_dict[name]["score"] = score

website_html_request = requests.get(url="https://news.ycombinator.com/news")
website_html = website_html_request.text

soup = BeautifulSoup(markup=website_html, features="html.parser")

a_tags = dict()

for a_tag in soup.select(selector="span.titleline > a"):
    title = a_tag.string
    a_tags[title] = dict()
    a_tags[title]["link"] = a_tag["href"]

a_tag_tup = list(a_tags.items())

tag_count = 0

for span in soup.select(selector="span.score"):
    score = int(span.string.split()[0])

    add_score(a_tags, a_tag_tup, score, tag_count)

    tag_count += 1

if tag_count < len(a_tag_tup):
    for i in range(tag_count, len(a_tag_tup)):
        score = 0

        add_score(a_tags, a_tag_tup, score, tag_count)

a_list = sorted(a_tags, key=lambda x: a_tags[x]["score"], reverse=True)

print(a_tags[a_list[0]])
