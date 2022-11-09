import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
# from sqlalchemy import create_engine
URL = 'https://universitypress.whiterose.ac.uk/site/books/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

books = soup.find_all("ul", class_ = "book-list")
# print((books))
# book_title = books[0].find("meta", {"itemprop":"name"}).get("content")
book_author = books[0].find("div", class_ = "description").find("a").text

# book_format = books[0].find("p", class_ = "format").text
# book_published = books[0].find("p", class_ = "published").text
# book_isbn = books[0].find("a", class_ = "btn btn-sm btn-primary add-to-basket").get("data-isbn")
# book_currency = books[0].find("a", class_ = "btn btn-sm btn-primary add-to-basket").get("data-currency")
# book_price = books[0].find("a", class_ = "btn btn-sm btn-primary add-to-basket").get("data-price")
print(book_author)