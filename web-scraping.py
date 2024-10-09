from bs4 import BeautifulSoup
from csv import writer
import requests
import time


headerParams = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

base_url = "https://www.trendyol.com"
url_to_search = "https://www.trendyol.com/bilgisayar-x-c108656" ##URL ADDRESS YOU WANT TO SCAN



with open("product.csv", "w", encoding="utf-8", newline='') as productFile:
    csv_writer = writer(productFile)
    csv_writer.writerow(["link","title","brand","modelNu","price"])

    page = 1

    while True:
        url = f"{url_to_search}?pi={page}"
        response = requests.get(url, headers=headerParams)
        
        
        if response.status_code != 200:
            print(f"page {page} not found")
            break


        html = BeautifulSoup(response.text, "html.parser")
        products = html.find(class_="prdct-cntnr-wrppr").find_all(class_="p-card-wrppr with-campaign-view")


        for product in products:
            anchor = product.find(class_="product-down")
            # body_info = anchor.find("a").find(class_="prdct-desc-cntnr").find("h3").find(class_="product-desc-sub-text").string
            link = base_url + anchor.find("a").get("href")
            title = anchor.find("a").find(class_="prdct-desc-cntnr").find("h3").find(class_="product-desc-sub-container").string
            brand = anchor.find("a").find(class_="prdct-desc-cntnr").find("h3").find(class_="prdct-desc-cntnr-ttl").string
            modelNu = anchor.find("a").find(class_="prdct-desc-cntnr").find("h3").find(class_="prdct-desc-cntnr-name").string
            price = float(anchor.find(class_="prc-box-dscntd").text.replace("TL","").replace(".","").replace(",","."))

            csv_writer.writerow([link,title,brand,modelNu,float(price)])

        page +=1
        time.sleep(2)
