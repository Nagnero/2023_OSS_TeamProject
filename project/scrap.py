import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "https://finance.naver.com/sise/lastsearch2.naver"
filename = "1-30.csv"
#f = open(filename, "w", encoding="utf-8-sig", newline="")
#writer = csv.writer(f)

res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

data_rows = soup.find("table", attrs={"class":"type_5"}).find_all("tr")

with open(filename, "w", encoding="utf-8-sig", newline="") as file:
  writer = csv.writer(file)
  # save 30 stock data to csv
  for row in data_rows:
    # check the row has valid data
    no_column = row.find_all("td")
    if len(no_column) <= 1:   # 의미 없는 데이터 skip
      continue
    data = [column.get_text().strip() for column in no_column]
    writer.writerow(data)

# save filtered stock
filtered_data = []

with open("1-30.csv", "r", newline="", encoding="utf-8") as file:
  reader = csv.reader(file)
  print(reader)
  for row in reader:
    if row[5] and any(sign in row[5] for sign in ['+', '-']):
      change = float(row[5].replace("+", "").replace("-", "").replace("%", "").strip())
      if abs(change) >= 10.0:
        filtered_data.append(row)

# 필터링된 데이터를 새로운 CSV 파일에 씀
with open("filtered_data.csv", "w", newline="", encoding="utf-8") as outfile:
  writer = csv.writer(outfile)
    
  # 필터링된 데이터를 쓰기
  writer.writerows(filtered_data)


# browser search
# browser = webdriver.Chrome()
# browser.get("http://naver.com")

# elem = browser.find_element_by_id("query")
# elem.send_keys("z")
# elem.sec_keys(Keys.ENTER)
# browser.exit()

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