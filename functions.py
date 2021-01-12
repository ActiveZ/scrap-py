import pandas as pd
from quote import Quote
from shutil import copy


################################## SCRAPPING ##################################################


# récupération des objets quotes de chaque page
# retourne le tableau d'objets complété
def get_quotes(arr_quotes, soup, address):
    nb_quotes = len(arr_quotes)

    quotes = soup.find_all("span", attrs={"class": "text", "itemprop": "text"})
    # instanciation de l'objet quote avec son attribut content
    # et enregistrement du fichier dans resultats/quotes.txt
    for quote in quotes:
        quote_obj = Quote(quote.text)
        arr_quotes.append(quote_obj)


    authors = soup.find_all("small", attrs={"class": "author", "itemprop": "author"})
    i = nb_quotes
    for author in authors:
        arr_quotes[i].author = author.text
        i += 1


    tags = soup.find_all("meta", attrs={"class": "keywords", "itemprop": "keywords"})
    # complétion du tableau d'objets quotes (ajout du tableau de tags de la citation)
    i = nb_quotes
    for tag in tags:
        arr_quotes[i].tags = tag["content"].split(",")
        i += 1

    print ("Scrapping terminé à l'adresse " + address)
    return arr_quotes


################################## QUOTES ##################################################


# enregistrement du fichier dans resultats/quotes.txt
def print_quotes(arr_quotes):
    f = open("resultats/quotes.txt", "w", encoding="utf-8")
    for q in arr_quotes:
        f.write(q.content + "\n")
    f.close()
    print("Fichier quotes.txt enregistré")


################################## AUTHORS ##################################################


def print_authors(arr_quotes):
    arr_authors = []
    for q in arr_quotes:
        arr_authors.append(q.author)

    # élimination des doublons et tri alphabétique
    arr_authors = list(set(arr_authors))
    arr_authors.sort()

    # enregistrement dans fichier authors.txt
    f = open("./authors/authors.txt", "w", encoding="utf-8")
    for author in arr_authors:
        f.write(author + "\n")
    f.close()

    # enregistrement du fichier dans resultats/quotes.txt
    copy ("./authors/authors.txt", "./resultats")

    # création du fichier xlsx
    df = pd.DataFrame([arr_authors]).T
    df.to_excel(excel_writer="authors_book.xlsx", index=False,
                header=False, sheet_name='Authors')
    print("fichier authors_books.xlsx enregistré")


################################## TAGS ##################################################


def print_tags(arr_quotes):
    list_tags = [] # liste des tags
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
    copy ("./tags/tags.txt", "./resultats")
    print ("Fichier tag.txt enregistré")


################################## RESULTS ##################################################


def print_results(arr_quotes):
    # enregistrement des citations complètes dans fichier quotes.md
    f = open("./quotes/quotes.md", "w", encoding="utf-8")
    for quote_obj in arr_quotes:
        f.write("**Quote:**" + " " + quote_obj.content + "\n" +
                "Author: " + quote_obj.author + "\n" +
                "Tags: " + ", ".join(quote_obj.tags) + "\n\n")
    f.close()
    print ("Fichier quotes.md enregistré")