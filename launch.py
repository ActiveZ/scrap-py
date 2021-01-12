import os
import requests
from functions import get_quotes, print_quotes, print_authors, print_tags, print_results
from bs4 import BeautifulSoup
from quote import Quote


os.system('cls')
print("Scrapper lancé...")

# URL = "https://quotes.toscrape.com"
# r = requests.get(URL)
# soup = BeautifulSoup(r.content, "html.parser")
# main(soup)

# page = soup.find("li", attrs={"class": "next"})
# while page != None:
#     print("page:", page)
#     link = page.find("a")
#     print("href:",link.get('href'))
#     page = soup.find("li", attrs={"class": "next"})

arr_quotes = []  # tableau des citations + auteurs + tags

URL = "https://quotes.toscrape.com"
r = requests.get(URL)
soup = BeautifulSoup(r.content, "html.parser")
arr_quotes = get_quotes(arr_quotes, soup, URL) # 1ere page

# for q in arr_quotes:
#     print (q.content, q.author, q.tags)

# recherhe de la page suivante dans la page en cours
page = soup.find("li", attrs={"class": "next"}) 
while page != None:
    # print("page:", page)
    link = page.find("a")
    address = URL + link.get('href')
    # print("link:", URL + link.get('href'))
    r = requests.get(address)
    soup = BeautifulSoup(r.content, "html.parser")
    arr_quotes = get_quotes(arr_quotes, soup, address)
    page = soup.find("li", attrs={"class": "next"}) 


print_quotes(arr_quotes)

print_authors(arr_quotes)

print_tags(arr_quotes)

print_results(arr_quotes)

for q in arr_quotes: print (q.content, q.author, q.tags)