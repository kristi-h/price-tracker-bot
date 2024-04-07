import smtplib
import requests
import lxml
import os
from bs4 import BeautifulSoup

MY_SMTP= "smtp.gmail.com"
MY_EMAIL= os.environ.get("MY_SMTP_EMAIL")
MY_PW= os.environ.get("SMTP_EMAIL_PW")
TO_EMAIL= os.environ.get("TESTER_TO_EMAIL")

url= "https://www.amazon.com/Z-Man-Games-ZM7240-Terra-Mystica/dp/B00APPE4HK/ref=sr_1_1?crid=UE774Z8R0RAS&dib=eyJ2IjoiMSJ9.3y47cyVel_B5e-yEMw4KQaTydOeO7o8yL0EN_IyBlJl_OJ7fF0rqFymibeJOQK2FnhgwTmaUn0cATnKxAbP2gDX9hrfg58b0xmXtuXgKv8zKoZrGmQL1K8WrOxnYqRQnNonElt7R01gPZ5bH6HwmWYkL2Q3nmncKqtTTbGWYxmnZWB_SPoGJtA11AvNzciH1Q0Su7Sskxh9SICseSH2at6AiJXO10EPXIt-L7y9ojOF0VuV5CfJ2o23Mlp8GtHH8jPcsPsKJm0kHi-QMhlWbr6hDA9e3fiwruiyMuuZ_hP8.Pq5U1ER72_N5IEZqWP7614dDgg0xvin-EuNLPe3PcPY&dib_tag=se&keywords=terra%2Bmystica%2Bboard%2Bgame&qid=1712438651&sprefix=terra%2Bmystica%2Caps%2C164&sr=8-1&th=1"
header= {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response= requests.get(url, headers= header)

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

price= soup.find(class_="a-offscreen").get_text()
naked_price_float= float(price.split("$")[1])
print(naked_price_float)

prod_name= soup.find(id="productTitle").get_text().strip()
print(prod_name)

BUY_PRICE = 60

if naked_price_float <= BUY_PRICE:
    message= f"{prod_name} is now {price}. Now is the time to buy!"

    with smtplib.SMTP(MY_SMTP, port=587) as connection:
        connection.starttls()
        result = connection.login(MY_EMAIL, MY_PW)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"Subject: Amazon price drop on {prod_name}!\n\n{message}\n{url}".encode("utf-8")
        )