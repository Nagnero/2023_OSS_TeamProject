import csv
import requests
from bs4 import BeautifulSoup

stock_names = []
rates = []

url = "https://finance.naver.com/sise/lastsearch2.naver"

filename = "1-30.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")
#print(soup.find("table", attrs={"class":"type_5"}).find_all("tr"))
data_rows = soup.find("table", attrs={"class":"type_5"}).find_all("tr")

for row in data_rows:
  # check the row has valid data
  no_column = row.find_all("td")
  if len(no_column) <= 1:   # 의미 없는 데이터 skip
    continue
  data = [column.get_text().strip() for column in no_column]
  writer.writerow(data)



    #print(data)
  # if no_column:
  #   anchor_tag = row.find("a")
  #   # append valid data to array
  #   if anchor_tag:
  #     writer.writerow(anchor_tag)
  #     # save stock name
  #     stock_names.append(anchor_tag.text)
      
  #     # save flunctuate rate
  #     rate_column = row.find_all("td", attrs={"class":"number"})
  #     rates.append(rate_column[3].find("span").text.strip())
      


# for stock in stock_names:
#   print(stock)

# for rate in rates:
#   print(rate)