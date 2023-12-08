import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time

result_name = []
result_m_cap = []
result_price = []
result_rate = []
result_news_info = []
# save filtered stock data
filtered_data = []

url = "https://finance.naver.com/sise/lastsearch2.naver"

res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

data_rows = soup.find("table", attrs={"class":"type_5"}).find_all("tr")

# save 30 stock data to csv
for row in data_rows:
  # check the row has valid data
  no_column = row.find_all("td")
  if len(no_column) <= 1:   # no meaning skip
    continue
  temp_url = "https://finance.naver.com" + row.find("a").get("href")
  data = [column.get_text().strip() for column in no_column]
  data.append(temp_url)

  change = float(data[5].replace("+", "").replace("-", "").replace("%", "").strip())
  if abs(change) >= 5.0:
    filtered_data.append(data)

for row in filtered_data:
  res = requests.get(row[-1])
  soup = BeautifulSoup(res.text, "lxml")
  # save stock name
  result_name.append(row[1])
  # save rate
  result_rate.append(row[5])

  # get market capitalization
  m_cap = soup.find("table", attrs={"summary":"시가총액 정보"})
  m_cap_val = m_cap.find("em",id="_market_sum").get_text(strip=True)
  m_cap_val = m_cap_val.replace("\t", "").replace("\n", "") + "억원"
  if "조" in m_cap_val:
    m_cap_val = m_cap_val.replace("조", "조 ")
  result_m_cap.append(m_cap_val)

  # get price
  price_info = soup.find("div", attrs={"class":"rate_info"}).find("p", attrs={"class":"no_today"})
  price = price_info.find("span", attrs={"class":"blind"})
  result_price.append(price.text)

  #get related news
  news_section = soup.find("div", class_="news_section")
  if news_section:
    get_news = False
    news_info = {} # 뉴스제목과 링크 저장 딕셔너리
    news_list = news_section.find_all("li")  # 모든 뉴스 항목을 찾음
    for news_item in news_list:
      news_title = news_item.find("a").get_text(strip=True)
      if news_title.find("특징주") != -1:
        news_link = news_item.find("a")["href"]
        parsed_url = urlparse(news_link)
        query_params = parse_qs(parsed_url.query)
        article_id = query_params.get('article_id', [''])[0]
        office_id = query_params.get('office_id', [''])[0]
        temp_url = "https://n.news.naver.com/mnews/article/" + office_id + "/" + article_id
        # 해당 링크로 들어가 뉴스 타이틀 가져오기
        temp_res = requests.get(temp_url, allow_redirects=True)
        temp_res.raise_for_status()
        temp_soup = BeautifulSoup(temp_res.text, "lxml")
        temp_title = temp_soup.find("h2", attrs={"id":"title_area"}).text
        # 후처리 데이터 딕셔너리에 삽입 후 배열에 저장
        news_info["title"] = temp_title
        news_info["link"] = "https://n.news.naver.com/mnews/article/" + office_id + "/" + article_id
        result_news_info.append(news_info)
        get_news = True
        break
    if get_news == False:
      result_news_info.append(news_info)

cnt = 0
for item in filtered_data:
  print(result_name[cnt])
  print(result_m_cap[cnt])
  print(result_rate[cnt])
  print(result_price[cnt])
  print(result_news_info[cnt])
  cnt += 1

import json

# JSON으로 변환할 데이터
data = {
  "result_m_cap": result_m_cap,
  "result_price": result_price,
  "result_news_info": result_news_info
}

# JSON으로 변환
json_data = json.dumps(data, ensure_ascii=False)

# 변환된 JSON 출력 또는 다른 곳으로 전달
print(json_data)