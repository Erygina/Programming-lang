import requests
from bs4 import BeautifulSoup
from threading import Thread
from time import sleep
from model import News
from queue import Queue

# Общая функция для всех сайтов
def default_fun(url):
  ret = requests.get(url)
  retdata = ret.text
  return BeautifulSoup(retdata, features="html.parser")

# Получение новостей с сайта Mail Ru
def get_mailru_news():
  soup = default_fun("https://news.mail.ru/economics/")
  news_list_result=[]
  if not soup:
    exit(0)
  if soup.head:
    print(soup.head.find('title').string, flush=True)
  for news in soup.find_all('div', class_='newsitem newsitem_height_fixed js-ago-wrapper js-pgng_item'):
    title_el = news.find('span', class_='newsitem__title-inner')
    annotation_el = news.find('span', class_='newsitem__text')
    author_el = news.find('span', class_='newsitem__param')
    news_list_result.append(
      News(
        webSiteName = "https://news.mail.ru/economics/",
        title=title_el.text.strip(),
        annotation=annotation_el.text.strip(),
        author=author_el.text.strip()
      )
    )
  return news_list_result

# Получение новостей с сайта Yahoo
def get_yahoo_news():
  soup = default_fun("https://www.yahoo.com/")
  news_list_result = []
  if not soup:
    exit(0)
  if soup.head:
    print(soup.head.find('title').string, flush=True)
  for news in soup.find_all('div', class_='D(f) Fld(c) Fxg(1) Miw(0)'):
    title_el = news.find('h3', class_='LineClamp(2,2.6em) Mend(50px) Mb(4px) Lh(1.33) Fz(18px) Fz(16px)--maw1024 Fw(b) stream-item-title')
    annotation_el = news.find('p', class_='finance-ticker-fetch-success_D(n) LineClamp(2,40px) sub-upsell-fetch-success_D(n) Fz(14px) Lh(1.43) C(--batcave) Mb(4px) Mend(50px) Mt(2px) Bxz(bb) Wob($break-word)')
    print(annotation_el.text.strip(), flush=True)
    author_el = news.find('span', class_='Ell')
    news_list_result.append(
      News(
        webSiteName = "https://www.yahoo.com/",
        title=title_el.text.strip(),
        annotation=annotation_el.text.strip(),
        author=author_el.text.strip()
      )
    )
  return news_list_result

# Получение новостей с сайта BuzzFeed
def get_buzzfeed_news():
  soup = default_fun("https://www.buzzfeednews.com/")
  news_list_result = []
  if not soup:
    exit(0)
  if soup.head:
    print(soup.head.find('title').string, flush=True)
  for news in soup.find_all('span', class_='newsblock-story-card__info xs-pr1 xs-block'):
    title_el = news.find('h2', class_='newsblock-story-card__title')
    annotation_el = news.find('p', class_='newsblock-story-card__description')
    author_el = news.find('span', class_='newsblock-story-card__byline')
    news_list_result.append(
      News(
        webSiteName = "https://www.yahoo.com/",
        title=title_el.text.strip(),
        annotation=annotation_el.text.strip(),
        author=author_el.text.strip()
      )
    )
  return news_list_result 

web_site_dict={
  'https://www.yahoo.com/': get_yahoo_news,
  'https://news.mail.ru/': get_mailru_news,
  'https://www.buzzfeednews.com/': get_buzzfeed_news,
}

def background_task(q):
  while True:
      for website, news_function in web_site_dict.items():
          q.put((website, news_function))
      sleep(0.5)


def process_website_news(website, news_function, shown_news):
  if website not in shown_news:
      shown_news.add(website)
      news = news_function()
      for news_item in news:
          print(news_item)

if __name__ == "__main__":
  q = Queue()
  background_thread = Thread(target=background_task, args=[q], daemon=True)
  shown_news = set()
  try:
      background_thread.start()
      while True:
          if not q.empty():
            website, news_function = q.get()
            process_website_news(website, news_function, shown_news)
          else:
              sleep(0.5)
  except (KeyboardInterrupt, SystemExit):
    exit()
