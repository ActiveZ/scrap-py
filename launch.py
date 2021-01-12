import os
import requests
from functions import main
from bs4 import BeautifulSoup


os.system('cls')


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

URL = "https://quotes.toscrape.com"
r = requests.get(URL)
soup = BeautifulSoup(r.content, "html.parser")
main(soup) # 1ere page

# recherhe de la page suivante dans la page en cours
page = soup.find("li", attrs={"class": "next"}) 
while page != None:
    print("page:", page)
    link = page.find("a")
    print("link:",link.get('href'))
    r = requests.get(URL + link.get('href'))
    soup = BeautifulSoup(r.content, "html.parser")
    main(soup)
    # page = soup.find("li", attrs={"class": "next"})