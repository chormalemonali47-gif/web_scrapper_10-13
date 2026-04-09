import requests
from bs4 import BeautifulSoup
import pandas as pd
from database import insert_data

URL = "https://books.toscrape.com/"

def scrape_data():
    try:
        r = requests.get(URL)
        r.raise_for_status()  # ✅ catch HTTP errors

        soup = BeautifulSoup(r.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        data = []

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text

            data.append([title, price])

            # insert into database
            insert_data(title, price)

        df = pd.DataFrame(data, columns=["Title", "Price"])

        # ✅ append without repeating header
        df.to_csv("data/data.csv", mode="a", index=False, header=False)

        return df

    except Exception as e:
        print("Error in scraping:", e)
        return pd.DataFrame()