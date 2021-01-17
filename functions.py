import requests
import pandas as pd
from bs4 import BeautifulSoup
from quote import Quote
from shutil import copy

# -------------------------- AUTHOR INFOS --------------------------------------

# récupération des infos de l'auteur sur la page spécifique (about)


def get_author_infos(link):
    url = "https://quotes.toscrape.com" + link.get('href')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    born_date = soup.find("span", attrs="author-born-date").text
    born_location = soup.find("span", attrs="author-born-location").text
    description = soup.find("div", attrs="author-description").text
    return {"born_date": born_date,
            "born_location": born_location,
            "description": description}


# --------------------------- SCRAPPING ------------------------------


# récupération des objets quotes de chaque page
# retourne le tableau d'objets complété
def get_quotes(arr_quotes, soup, address):
    nb_quotes = len(arr_quotes)

    quotes = soup.find_all("span", attrs={"class": "text", "itemprop": "text"})
    # instanciation de l'objet quote avec son attribut content
    for quote in quotes:
        quote_obj = Quote(quote.text)
        arr_quotes.append(quote_obj)

    authors = soup.find_all(
        "small", attrs={"class": "author", "itemprop": "author"})
    i = nb_quotes
    for author in authors:
        author_infos = get_author_infos(author.find_next("a"))
        arr_quotes[i].author["name"] = author.text
        arr_quotes[i].author["born_date"] = author_infos["born_date"]
        arr_quotes[i].author["born_location"] = author_infos["born_location"]
        arr_quotes[i].author["description"] = author_infos["description"]
        i += 1

    tags = soup.find_all(
        "meta", attrs={"class": "keywords", "itemprop": "keywords"})
    # complétion du tableau d'objets quotes (ajout du tableau de tags)
    i = nb_quotes
    for tag in tags:
        arr_quotes[i].tags = tag["content"].split(",")
        i += 1

    print("Scrapping terminé à l'adresse " + address)
    return arr_quotes


# -------------------------- QUOTES --------------------------------------


# enregistrement du fichier dans resultats/quotes.txt
def print_quotes(arr_quotes):
    f = open("resultats/quotes.txt", "w", encoding="utf-8")
    for q in arr_quotes:
        f.write(q.content + "\n")
    f.close()
    print("Fichier quotes.txt enregistré")


# -------------------------- AUTHORS --------------------------------------
def print_authors(arr_quotes):
    arr_authors = []
    for q in arr_quotes:
        if(arr_authors.count(q.author) == 0):
            arr_authors.append(q.author)

    # tri de laliste des auteurs par ordre alphabétique de leur nom
    arr_authors = sorted(arr_authors, key=lambda author: author["name"])

    # enregistrement dans fichier authors.txt
    f = open("./authors/authors.txt", "w", encoding="utf-8")
    for author in arr_authors:
        f.write(author["name"] + " -- born: " + author["born_date"] + " " +
                author["born_location"] + "\n")
    f.close()

    # enregistrement du fichier dans resultats/quotes.txt
    copy("./authors/authors.txt", "./resultats")

    # création du fichier xlsx
    data = {"name": [], "description": []}
    for author in arr_authors:
        data["name"].append(author["name"])
        data["description"].append(author["description"])
    df = pd.DataFrame({"NAMES": data["name"],
                       "DESCRIPTIONS": data["description"]})
    df.to_excel(excel_writer="authors_book.xlsx", index=False,
                header=True, sheet_name='Authors')
    print("fichier authors_books.xlsx enregistré")


# ------------------------- TAGS ----------------------------------------


def print_tags(arr_quotes):
    list_tags = []  # liste des tags
    for q in arr_quotes:
        list_tags.extend(q.tags)

    # élimination des doublons et tri alphabétique de la liste des tags
    list_tags = list(set(list_tags))
    list_tags.sort()

    # enregistrement dans fichier tags.txt
    f = open("./tags/tags.txt", "w", encoding="utf-8")
    for tag in list_tags:
        f.write(tag + "\n")
    f.close()

    # enregistrement du fichier dans resultats/quotes.txt
    copy("./tags/tags.txt", "./resultats")
    print("Fichier tag.txt enregistré")


# ------------------------------ RESULTS -----------------------------------


def print_results(arr_quotes):
    # enregistrement des citations complètes dans fichier quotes.md
    f = open("./quotes/quotes.md", "w", encoding="utf-8")
    f.writelines(["|Quote|Author|Tags|\n", "|:---|:---:|---|\n"])
    for quote_obj in arr_quotes:
        f.writelines(["|" + quote_obj.content + "|" +
                      quote_obj.author["name"] + "|" +
                      ", ".join(quote_obj.tags) + "|\n"])
    f.close()
    print("Fichier quotes.md enregistré")
