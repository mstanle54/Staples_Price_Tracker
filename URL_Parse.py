import re

import requests
from bs4 import BeautifulSoup

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
        r= requests.get(url)
        soup = BeautifulSoup(page.content, "html5lib")

        #may not need to .get_text() here. see if it messes anything
        title = soup.find ('h1', {'id' :'product_title'}).get_text()

        print("Title is: %s"  % title)

        details["name"] = title

        price= soup.find(class_="price-info__final_price")

        #let's print the whole html thing...whatever it's called
        print (price)
        print "yas?"
        #I suppose the price is the only actual text in that html code, so we can simply .get_text()
        print("Here it is girly "+price.get_text())
        details["price"] = get_converted_price(price.get_text())
        print ("Price: $%s"  % details["price"])
        print (type(details["price"]))
        #trying to verify that the price is a float
        #print ("Price with badass 50% discount: $" + (details["price"])/2)

        #price = soup.find(class="price_section")


       # price = soup.find(id="priceBlockStrikePriceString")
        #What should this case be for Staples?
        if price is None:
            print "price is None"

            price = soup.find(id="priceblock_ourprice")
            details["deal"] = False

        if title is not None and price is not None:
            #details["name"] = title.get_text().strip()
            details["name"] = title
            details["price"] = get_converted_price(price.get_text())
            details["url"] = _url

        else:
            return None
        return details

def extract_url(url):
    if url.find("www.staples.com/") != -1:
        #some products have 6 identifying digits, some have 7 or 8
        index = url.find("/product_")

        if index == -1:
            #must not be a product
            print "idk what you're problem is man. You made it to Staples.com, but clearly can't tell what a product is"
            url = None
        else:
            product_num = url.split("product_")[-1]
            url = "https://www.staples.com/product_" + product_num
            print ("simplified url: "+ url)
            return url
    else:
        print "This ain't no Staples.com, buddy. Try again."
        url = None
    return url

#do I need this function for Staples.com? what exactly is its purpose?
def get_converted_price(price):

    # stripped_price = price.strip("$ ,")
    # replaced_price = stripped_price.replace(",", "")
    # find_dot = replaced_price.find(".")
    # to_convert_price = replaced_price[0:find_dot]
    # converted_price = int(to_convert_price)
    #simplified with regex
    converted_price = float(re.sub(r"[^\d.]", "", price))
    return converted_price

def print_product_details(extracted_details):
    print("\n" +extracted_details["name"] + "\n" +
          "Price: $%s"  % extracted_details["price"] + "\n" +
          "On Sale?: %r" % extracted_details["deal"])

#product_url = raw_input("Enter URL of product:")
product_url = "https://www.staples.com/Post-it-Notes-Canary-Yellow-3-x-3-12-Pads-Pack-654-12YW/product_130005"
#extract_url(product_url)
get_product_details(product_url)
print_product_details(get_product_details(product_url))
