import requests
from bs4 import BeautifulSoup

URL = "https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
website_request = requests.get(url=URL)
website_html = website_request.text

soup = BeautifulSoup(markup=website_html, features="html.parser")

movies = list()

for title in soup.select("span > h2 > strong"):
    movies.append(title.string)

with open("Top 100 Movies.txt", mode="w", encoding="UTF-8") as file:
    for movie in movies[::-1]:
        file.write(f"{movie}\n")





