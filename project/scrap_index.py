import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time

url_index = ["https://kr.investing.com/indices/kospi",
            "https://kr.investing.com/indices/kosdaq",
            "https://kr.investing.com/indices/nq-100",
            "https://kr.investing.com/indices/us-spx-500",
            "https://kr.investing.com/indices/us-30",
            "https://kr.investing.com/indices/hang-sen-40",
            "https://kr.investing.com/indices/phlx-semiconductor",
            "https://kr.investing.com/indices/baltic-dry",
            "https://kr.investing.com/indices/volatility-s-p-500",
            "https://kr.investing.com/rates-bonds/us-10-yr-t-note",
            "https://kr.investing.com/rates-bonds/us-2-yr-t-note",
            "https://kr.investing.com/crypto/bitcoin",
            "https://kr.investing.com/equities/tesla-motors",
            "https://kr.investing.com/equities/nvidia-corp"]

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

for url in url_index:
    get_value_from_investing(url)

print(result_price)
print(result_data)
print(result_gap)
print(result_rate)