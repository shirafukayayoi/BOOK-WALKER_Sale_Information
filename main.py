import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import csv
from datetime import datetime

def main():
    scraping = WebScraping()
    data = scraping.get_html()
    if data:
        csv_writer = CSVWriter()
        csv_writer.write_data(data)

class WebScraping:
    def __init__(self):
        self.base_url = "https://bookwalker.jp/category/2/?order=rank&detail=1&qpri=2&qspp=1&qcsb=1&np=1"
        self.endpage = 0
        self.title_list = []
        self.author_list = []
        self.money_list = []
        self.label_list = []
        self.enddate_list = []
        self.query_params = {
            "page": "{}"
        }
        self.session = requests.Session()
        retry = Retry(connect=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get_html(self):
        try:
            req = self.session.get(self.base_url)
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"初回リクエストでエラーが発生しました: {e}")
            return

        req.encoding = req.apparent_encoding
        html_soup = BeautifulSoup(req.text, "html.parser")

        # ページ数を取得
        pager_boxes = html_soup.find_all(class_="o-pager-box-num")
        if pager_boxes:
            # 最後のページ番号を取得
            self.endpage = int(pager_boxes[-1].get_text())
        else:
            print("ページ数を取得できませんでした")
            return

        # 各ページのデータを取得
        for page in range(1, int(self.endpage) + 1):
            self.query_params["page"] = str(page)
            url = self.base_url + "&" + urlencode(self.query_params)
            try:
                req = self.session.get(url)
                req.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"{page}ページ目のリクエストでエラーが発生しました: {e}")
                continue

            req.encoding = req.apparent_encoding
            html_soup = BeautifulSoup(req.text, "html.parser")
            titles = html_soup.find_all(class_="o-card-ttl__text")
            authors = html_soup.find_all('a', {'data-action-label': '著者名'})
            moneys = html_soup.find_all(class_="m-book-item__price-num")
            labels = html_soup.find_all('a', {'data-action-label': 'レーベル名'})
            enddates = html_soup.find_all(class_="a-card-period")

            if titles and authors and labels and enddates and moneys:
                for title, author, label, enddate, money in zip(titles, authors, labels, enddates, moneys):
                    self.title_list.append(title.get_text().strip())
                    self.author_list.append(author.get_text().strip())
                    self.money_list.append(money.get_text().strip())
                    self.label_list.append(label.get_text().strip())
                    formatted_date = self.format_date(enddate.get_text().strip())
                    self.enddate_list.append(formatted_date)
                    print(f"{len(self.enddate_list)}件目のデータを取得しました")

        # データの総数を表示
        print(f"タイトルの数: {len(self.title_list)}")
        print(f"著者の数: {len(self.author_list)}")
        print(f"レーベルの数: {len(self.label_list)}")
        print(f"終了日の数: {len(self.enddate_list)}")

        data = [(self.title_list[i], self.author_list[i], self.money_list[i], self.label_list[i], self.enddate_list[i]) for i in range(len(self.title_list))]
        return data
    
    def format_date(self, date_str):
        input_date = date_str.split('(')[0]
        try:
            date_obj = datetime.strptime(input_date, '%Y/%m/%d')
            formatted_date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            print(f"日付のパースに失敗しました: {date_str}")
        return formatted_date

class CSVWriter:
    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.filename = f"BOOK☆WALKER_{self.today}_SalesList.csv"
    
    def write_data(self, data):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["タイトル", "著者", "金額", "レーベル", "終了日"])
            writer.writerows(data)

if __name__ == "__main__":
    main()
