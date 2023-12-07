const axios = require('axios');
const cheerio = require('cheerio');
const { URLSearchParams } = require("url");
const iconv = require('iconv-lite');

let result_name = [];
let result_m_cap = [];
let result_price = [];
let result_rate = [];
let result_news_info = [];
let filtered_data = [];

const url = "https://finance.naver.com/sise/lastsearch2.naver";

axios
  .get(url, {responseType: "arraybuffer"})
  .then((response) => {
    const body = response.data;
    const html = iconv.decode(body, "EUC-KR").toString()
    const $ = cheerio.load(html);
    const dataRows = $("table.type_5 tr");
    console.log(html);
    dataRows.each((index, element) => {
      const columns = $(element).find("td");
      if (columns.length <= 1) return;

      const temp_url =
        "https://finance.naver.com" + $(element).find("a").attr("href");
      const data = columns.map((i, column) => $(column).text().trim()).get();
      data.push(temp_url);

      const change = parseFloat(
        data[5].replace("+", "").replace("-", "").replace("%", "").trim()
      );
      if (Math.abs(change) >= 5.0) {
        filtered_data.push(data);
      }
    });
    filtered_data.forEach((row) => {
      axios
        .get(row[row.length - 1])
        .then((response) => {
          const htmlData = response.data;
          const $ = cheerio.load(htmlData);

          result_name.push(row[1]);
          result_rate.push(row[5]);

          const m_cap = $("table[summary='시가총액 정보']");
          let m_cap_val =
            m_cap.find("em#_market_sum").text().replace(/\t|\n/g, "") + "억원";
          if (m_cap_val.includes("조")) {
            m_cap_val = m_cap_val.replace("조", "조 ");
          }
          result_m_cap.push(m_cap_val);

          const price_info = $("div.rate_info p.no_today");
          const price = price_info.find("span.blind").text();
          result_price.push(price);

          const news_section = $("div.news_section");
          if (news_section.length) {
            let get_news = false;
            const news_info = {};
            const news_list = news_section.find("li");

            news_list.each((index, news_item) => {
              const news_title = $(news_item).find("a").text();
              if (news_title.includes("특징주")) {
                const news_link = $(news_item).find("a").attr("href");
                const urlParams = new URLSearchParams(news_link);
                const articleId = urlParams.get("article_id");
                const officeId = urlParams.get("office_id");
                const temp_url = `https://n.news.naver.com/mnews/article/${officeId}/${articleId}`;

                axios
                  .get(temp_url, { allow_redirects: true })
                  .then((tempResponse) => {
                    const tempHtml = tempResponse.data;
                    const temp$ = cheerio.load(tempHtml);
                    const tempTitle = temp$("#title_area").text();

                    news_info["title"] = tempTitle;
                    news_info[
                      "link"
                    ] = `https://n.news.naver.com/mnews/article/${officeId}/${articleId}`;
                    result_news_info.push(news_info);
                    get_news = true;
                  })
                  .catch((error) =>
                    console.error("Error fetching news:", error)
                  );

                if (get_news === false) {
                  result_news_info.push(news_info);
                }

                return false;
              }
            });
          }
        })
        .catch((error) => console.error("Error fetching data:", error));
    });
  })
  .catch((error) => console.error("Error:", error));