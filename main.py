import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/")
# soup = BeautifulSoup(r.content, "lxml")
soup = BeautifulSoup(r.content, "html.parser")

print("-------- CITATIONS --------")
citations = soup.find_all("span", attrs={"class":"text", "itemprop":"text"})
for citation in citations:
    print (citation.text)

print("-------- AUTHORS --------")
authors = soup.find_all("small", attrs={"class":"author", "itemprop":"author"})
for author in authors:
    print(author.text)

print("-------- TAGS --------")
tags = soup.find_all("a", attrs={"class":"tag"})
# print(tags.text)

# remplissage d'u tableau de tags
arr_tags = []
for tag in tags: arr_tags.append(tag.text)

# élimination des doublons et tri alphabétique
tags = list(set(arr_tags))
tags.sort()
# print(tags)

# impression dans fichier tags.txt
f = open("tags.txt", "w")
for tag in tags:
    # print(tag)
    f.write(tag + "\n")
f.close()