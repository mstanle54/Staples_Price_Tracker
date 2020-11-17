import re

import requests
from bs4 import BeautifulSoup

def extract_url(url):

    if url.find("www.amazon.com") != -1:
        #for staples, instead of dp it is product_
        #some products have 6 identifying digits, some have 7 or 8
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.com" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.com" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url



def get_converted_price(price):

    # stripped_price = price.strip("$ ,")
    # replaced_price = stripped_price.replace(",", "")
    # find_dot = replaced_price.find(".")
    # to_convert_price = replaced_price[0:find_dot]
    # converted_price = int(to_convert_price)
    #simplified with regex
    converted_price = float(re.sub(r"[^\d.]", "", price))
    return converted_price

def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)

    if _url is None:
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html5lib")
        title = soup.find(id="productTitle")
        price = soup.find(id="priceblock_dealprice")
       # price = soup.find(id="priceBlockStrikePriceString")

        if price is None:
            price = soup.find(id="priceblock_ourprice")
            details["deal"] = False

        if title is not None and price is not None:
            details["name"] = title.get_text().strip()
            details["price"] = get_converted_price(price.get_text())
            details["url"] = _url

        else:
            return None
        return details
        #return (print_product_details(details))

#print product details in an easy to read format
def print_product_details(extracted_details):
    print("\n" +extracted_details["name"] + "\n" +
          "Price: $%s"  % extracted_details["price"] + "\n" +
          "On Sale?: %r" % extracted_details["deal"])


product_url = raw_input("Enter URL of product:")

print_product_details(get_product_details(product_url))



#print(get_product_details("https://www.amazon.in/dp/B07HGJJ58K"))