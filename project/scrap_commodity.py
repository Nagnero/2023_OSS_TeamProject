import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time

url_metal = ["https://kr.investing.com/commodities/gold",
            "https://kr.investing.com/commodities/copper",
            "https://kr.investing.com/commodities/nickel?cid=959208",
            "https://kr.investing.com/commodities/aluminum",
            "https://kr.investing.com/commodities/palladium"]

url_food = ["https://kr.investing.com/commodities/us-wheat",
            "https://kr.investing.com/commodities/us-soybeans",
            "https://kr.investing.com/commodities/us-corn"]

url_resource = ["https://kr.investing.com/commodities/crude-oil",
                "https://kr.investing.com/commodities/natural-gas",
                "https://kr.investing.com/commodities/heating-oil",
                "https://kr.investing.com/commodities/gasoline-rbob"]

result_data = []
result_price = []
result_gap = []
result_rate = []

def get_value_from_investing(url):
  try:
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    temp_data = soup.find("h1", attrs={"class":"md:text-3xl"}).text
    temp_data_split = temp_data.split('-')
    temp_price = soup.find("div", attrs={"data-test":"instrument-header-details"})
    if temp_price:
      result_data.append(temp_data_split[0].strip())
      value = temp_price.find("div", class_="text-5xl/9").text.strip()
      result_price.append(value)
      result_gap.append(temp_price.find("span", attrs={"data-test":"instrument-price-change"}).text)
      result_rate.append(temp_price.find("span", attrs={"data-test":"instrument-price-change-percent"}).text)
      return value
  except Exception as e:
    print(f"An error occurred: {e}")
    return None

for url in url_metal:
  get_value_from_investing(url)

for url in url_food:
  get_value_from_investing(url)

for url in url_resource:
  get_value_from_investing(url)

print(result_price)
print(result_data)
print(result_gap)
print(result_rate)


