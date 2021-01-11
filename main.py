import requests
from citation import Citation
from bs4 import BeautifulSoup


r = requests.get("https://quotes.toscrape.com/")
soup = BeautifulSoup(r.content, "html.parser")
arr_citations = []

################################## CITATIONS ##################################################

print("-------- CITATIONS --------")
citations = soup.find_all("span", attrs={"class":"text", "itemprop":"text"})
for citation in citations:
    print (citation.text)
    citation = Citation(citation.text)
    arr_citations.append(citation)

################################## AUTHORS ##################################################

print("-------- AUTHORS --------")
f = open("authors.txt", "w")
authors = soup.find_all("small", attrs={"class":"author", "itemprop":"author"})
i = 0
for author in authors:
    arr_citations[i].author = author.text
    # print(author.text)
    f.write(author.text + "\n")
    i += 1
f.close()


################################## TAGS ##################################################

print("-------- TAGS --------")
tags = soup.find_all("meta", attrs={"class":"keywords", "itemprop":"keywords"})
# print(tags.text)


# remplissage d'un tableau de tags
arr_tags = []
for tag in tags: arr_tags.append(tag["content"])

i = 0
for tag in arr_tags:
    arr_citations[i].tags = tag
    i += 1

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


################################## RESULTS ##################################################

for citation in arr_citations: print("citation:", citation.content, "Auteur:", citation.author, "Tags:", citation.tags, "\n")