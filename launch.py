import os
import requests
from functions import get_quotes, print_quotes, print_authors, print_tags,\
     print_results
from bs4 import BeautifulSoup


os.system('cls')  # attention, sur ubuntu, remplacer par os.system('clear')
print("Scrapper lancé...")

arr_quotes = []  # tableau des citations + auteurs + tags
URL = "https://quotes.toscrape.com"
go_scrapping = True
url = URL

# parcours les pages tant qu'il y a des pages suivantes
while go_scrapping:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    arr_quotes = get_quotes(arr_quotes, soup, url)
    page = soup.find("li", attrs={"class": "next"})
    go_scrapping = page is not None
    if go_scrapping:
        link = page.find("a")
        url = URL + link.get('href')

print_quotes(arr_quotes)

print_authors(arr_quotes)

print_tags(arr_quotes)

print_results(arr_quotes)

# affichage des résultats
for q in arr_quotes:
    print(q.content, q.author, q.tags)
