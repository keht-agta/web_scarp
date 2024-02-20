import requests
from bs4 import BeautifulSoup
import fake_headers

def gen_headers():
    headers_gen = fake_headers.Headers(os= "win", browser="chrome")
    return headers_gen.generate()

def vacancy_info(web_link):
    html_data = requests.get(web_link, headers=gen_headers()).text
    soup= BeautifulSoup(html_data,  'lxml')
    #описание вакансии 
    #Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask"
    #<div class="g-user-content" data-qa="vacancy-description">
    # print(html_data)
    dict_vacancy ={}
    articles_tag = soup.find(attrs={'class':"g-user-content", 'data-qa':"vacancy-description"})
    if articles_tag:
        res_text = articles_tag.getText()
        if "Django" in res_text and "Flask" in res_text:
    # Записать в json информацию о каждой вакансии - 
    # ссылка - link_list
            dict_vacancy['link'] = web_link
        # Название вакансии <h1 data-qa="vacancy-title" class="bloko-header-section-1">
            articles_tag = soup.find(attrs={'class':"bloko-header-section-1", 'data-qa':"vacancy-title"})
            if articles_tag:
                res_text = articles_tag.getText()
                dict_vacancy['name'] = res_text
        # вилка зп <div data-qa="vacancy-salary"> -
        # <span data-qa="vacancy-salary-compensation-type-net" class="bloko-header-section-2 bloko-header-section-2_lite">
        # от <!-- -->35&nbsp;000<!-- --> до <!-- -->50&nbsp;000<!-- --> <!-- -->₽
        # <span class="vacancy-salary-compensation-type"> <!-- -->на руки</span></span>
            articles_tag = soup.find(attrs={'class':"bloko-header-section-2 bloko-header-section-2_lite", 'data-qa':"vacancy-salary-compensation-type-net"})
            if articles_tag:    
                res_text = articles_tag.getText()
                dict_vacancy['salary'] = res_text
        # название компании - <span class="vacancy-company-name"><a data-qa="vacancy-company-name" class="bloko-link bloko-link_kind-tertiary"
        #  href="/employer/10040283?hhtmFrom=vacancy"><span data-qa="bloko-header-2" class="bloko-header-section-2 bloko-header-section-2_lite">
        # <span>Championika Digital (Прохорова Ксения Владимировна)</span></span></a></span>
            articles_tag = soup.find(attrs={'class':"bloko-link bloko-link_kind-tertiary", 'data-qa':"vacancy-company-name"})
            if articles_tag:    
                res_text = articles_tag.getText()
                dict_vacancy['company_name'] = res_text
        # город- <span data-qa="vacancy-view-raw-address">Санкт-Петербург, 1 линия, метро Лесная</span></a></div>
            articles_tag = soup.find(attrs={'data-qa':"vacancy-view-raw-address"})
            if articles_tag:
                res_text = articles_tag.getText().split(',')[0]
                dict_vacancy['city'] = res_text
    return dict_vacancy

# vacancy_info(WEB)

# pprint(type(articles_list_tag))
# articles_list_tag = main_soup.find(name="div", class_="tm-articles-list")   

# for article_tag in articles_list_tag.find_all('article'):
#     h2_tag = article_tag.find('h2', class_='tm-title tm-title_h2')
#     a2_tag = h2_tag.find('a', class_='tm-title__link')
#     time_tag = article_tag.find('time')

#     header = h2_tag.text.strip()
#     link_relative = a2_tag['href']
#     link_absolute = f'https://habr.com{link_relative}'
#     publication_time = time_tag['datetime']