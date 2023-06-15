import json
import requests
from bs4 import BeautifulSoup


def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    url = "https://phys.org/space-news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all("article", class_="sorted-article")

    news_dict = {}
    for article in articles_cards:
        article_title = article.find("h3", class_="mb-1 mb-lg-2").text.strip()
        article_desc = article.find("p", class_="mb-1 pr-1").text.strip()
        article_url = article.find("a", class_="news-link").get("href")
        article_date_time = article.find("p", class_="text-uppercase text-low").text.strip()

        article_id = article_url.split("/")[-1]
        article_id = article_id[:-5]

        news_dict[article_id] = {
            "article_date_time": article_date_time,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    url = "https://phys.org/space-news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all("article", class_="sorted-article")

    fresh_news = {}
    for article in articles_cards:
        article_url = article.find("a", class_="news-link").get("href")
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-5]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h3", class_="mb-1 mb-lg-2").text.strip()
            article_desc = article.find("p", class_="mb-1 pr-1").text.strip()
            article_date_time = article.find("p", class_="text-uppercase text-low").text.strip()

            news_dict[article_id] = {
                "article_date_time": article_date_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

            fresh_news[article_id] = {
                "article_date_time": article_date_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    get_first_news()
    check_news_update()


if __name__ == '__main__':
    main()
