import csv
import requests
from bs4 import BeautifulSoup
import certifi

stock_names = []
rates = []

url = "https://finance.naver.com/sise/lastsearch2.naver"
#headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")
#print(soup.find("table", attrs={"class":"type_5"}).find_all("tr"))
data_rows = soup.find("table", attrs={"class":"type_5"}).find_all("tr")

for row in data_rows:
  # check the row has valid data
  no_column = row.find("td", attrs={"class":"no"})
  if no_column:
    anchor_tag = row.find("a")
    # append valid data to array
    if anchor_tag:
      # save stock name
      stock_names.append(anchor_tag.text)
      # save flunctuate rate
      rate_column = row.find_all("td", attrs={"class":"number"})
      rates.append(rate_column[3].find("span").text)


for stock in stock_names:
  print(stock)

for rate in rates:
  print(rate)