import json
from time import sleep
import requests
from bs4 import BeautifulSoup
import fake_headers
from pprint import pprint
from progress.bar import Bar
from modules.submain import vacancy_info


def gen_headers():
    headers_gen = fake_headers.Headers(os= "win", browser="chrome")
    return headers_gen.generate()


WEB = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page='
link_list=[]
count_page = int(input('Введите количество страниц для поиска вакансий. 20 вакансий на одной странице:'))
bar = Bar('Processing', max = 20*count_page)
print("Поиск вакансий")
for i in range(0,count_page):
    WEB_=f'{WEB}{i}'
    main_response = requests.get(WEB, headers=gen_headers())
    main_html_data = main_response.text
    main_soup= BeautifulSoup(main_html_data,  'lxml')
    articles_list_tag = main_soup.findAll(name="span", class_="serp-item__title-link-wrapper")   
    for article in articles_list_tag:
        link = article.find('a', class_="bloko-link")['href']
        bar.next()
        sleep(0.1)
        link_list.append(link)       
bar.finish()
print(f"По Вашему запросу найдено {len(link_list)} вакансий")
print("Отбираем список вакансий которые удовлетворяют ваши запросы")
# pprint (link_list) #список всех ссылок с первой страницы поиска
bar = Bar('Processing', max = 20*count_page)
json_data = []
for link in link_list:
    bar.next()
    result = vacancy_info(link)
    if result:
        json_data.append(result)
bar.finish()
print(f"Подходящие вакансии в количестве {len(json_data)} шт. были помещены в файл vacancy.json")
with open("data_file.json", "w",encoding='utf-8') as f:
    json.dump(json_data, f,ensure_ascii=False)
