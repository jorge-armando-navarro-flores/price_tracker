import requests
import smtplib
import os
from bs4 import BeautifulSoup
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
product_url = "https://www.amazon.com/Apple-MacBook-16-Inch-Storage-2-3GHz/dp/B085WSD2TN/ref=sr_1_3?crid=2WOKBHVQM1W09&keywords=macbook+pro&qid=1641316127&refinements=p_89%3AApple&rnid=2528832011&s=electronics&sprefix=macbook+pro%2Caps%2C265&sr=1-3"
response = requests.get(product_url, headers=headers)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")
price_tag = soup.select_one("tr td span span")
h1_tag = soup.select_one("h1 span")
product = h1_tag.text
price = float("".join(price_tag.text.split("$")[1].split(",")))
print(price)
target_price = 2800

from_email = os.environ.get("EMAIL")
from_password = os.environ.get("PASSWORD")
to_email = os.environ.get("TO_EMAIL")

if price < target_price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=from_email, password=from_password)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=to_email,
            msg=f"Subject:Amazon Price Alert!\n\n{product} is now ${price}"
        )
