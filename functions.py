# import os
# import requests
from bs4 import BeautifulSoup
import pandas as pd
from quote import Quote
from shutil import copy


# os.system('clear')

# URL = "https://quotes.toscrape.com/page/10"
# r = requests.get(URL)
# soup = BeautifulSoup(r.content, "html.parser")
arr_quotes = []  # tableau des citations + auteurs + tags

def main(soup):

    ################################## QUOTES ##################################################


    print("-------- QUOTES --------")
    quotes = soup.find_all("span", attrs={"class": "text", "itemprop": "text"})

    f = open("resultats/quotes.txt", "w")
    # instanciation de l'objet quote avec son attribut content
    # et enregistrement du fichier dans resultats/quotes.txt
    for quote in quotes:
        # print("quote_content:", quote.text)
        f.write(quote.text + "\n")
        quote_obj = Quote(quote.text)
        arr_quotes.append(quote_obj)
    f.close()


    ################################## AUTHORS ##################################################


    print("-------- AUTHORS --------")
    authors = soup.find_all("small", attrs={"class": "author", "itemprop": "author"})

    i = 0
    arr_authors = [] # tableau des auteurs
    for author in authors:
        arr_quotes[i].author = author.text
        arr_authors.append(author.text)
        # print(author.text)
        i += 1

    # élimination des doublons et tri alphabétique
    arr_authors = list(set(arr_authors))
    arr_authors.sort()
    # print("arr_author", arr_authors)

    # enregistrement dans fichier authors.txt
    f = open("./authors/authors.txt", "w")
    for author in arr_authors:
        f.write(author + "\n")
    f.close()

    # enregistrement du fichier dans resultats/quotes.txt
    copy ("./authors/authors.txt", "./resultats")

    # création du fichier xlsx
    df = pd.DataFrame([arr_authors]).T
    df.to_excel(excel_writer="authors_book.xlsx", index=False,
                header=False, sheet_name='Authors')


    ################################## TAGS ##################################################


    print("-------- TAGS --------")
    tags = soup.find_all(
        "meta", attrs={"class": "keywords", "itemprop": "keywords"})


    arr_tags = [] # tableau de tags à 2 dimensions
    list_tags = [] # liste des tags
    for tag in tags: 
        arr_tags.append(tag["content"])
        list_tags.extend(tag["content"].split(","))

    # complétion du tableau d'objets quotes (ajout du tableau de tags de la citation)
    i = 0
    for tag in arr_tags:
        arr_quotes[i].tags = tag
        i += 1


    # élimination des doublons et tri alphabétique de la liste des tags
    list_tags = list(set(list_tags))
    list_tags.sort()

    # enregistrement dans fichier tags.txt
    f = open("./tags/tags.txt", "w")
    for tag in list_tags:
        # print(tag)
        f.write(tag + "\n")
    f.close()

    # enregistrement du fichier dans resultats/quotes.txt
    copy ("./tags/tags.txt", "./resultats")


    ################################## RESULTS ##################################################


    # enregistrement des citations complètes dans fichier quotes.md
    f = open("./quotes/quotes.md", "w")
    for quote_obj in arr_quotes:
        f.write("**Quote:**" + quote_obj.content + "\n" +
                "Auteur:" + quote_obj.author + "\n" +
                "Tags:" + quote_obj.tags + "\n\n")
    f.close()


################################## PAGES ##################################################

# page = soup.find("li", attrs={"class": "next"})
# # while page != "None":
# print("page:", page)
# link = page.find("a")
# print("href:",link.get('href'))
# page = soup.find("li", attrs={"class": "next"})
