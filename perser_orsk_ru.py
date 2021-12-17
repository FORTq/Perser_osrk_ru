import json
import random
import time

import requests
from bs4 import BeautifulSoup
import fake_useragent


user = fake_useragent.UserAgent().random
header = {'user-agent':user}
prodeject_list = []
iter = 1
for i in range(38):
    url = (f'http://board.orsk.ru/index.php?r=category%2Findex&category_id=19&page={i}&per-page=100')
    res = requests.get(url,headers=header)
    soup = BeautifulSoup(res.text, 'lxml')
    items = soup.find('div',class_='container-items')
    obv = items.find_all('div',class_='item')
    print(iter)
    iter += 1
    for nuub, items in enumerate(obv):
        url = 'http://board.orsk.ru' + items.find('div',class_='title').find('a').get('href')
        res = requests.get(url,headers=header)
        soup = BeautifulSoup(res.text, 'lxml')
        items = soup.find('div',class_="item view-detail")
        try:
            vakansia = items.find('span',class_='val').text
        except Exception:
            vakansia = 'Неизвестно'
        try:
            zarplata = items.find('b', class_='s18').text
        except Exception:
            zarplata = 'Неизвестно'
        try:
            phone = soup.find('div',class_='phone').text.strip()
        except Exception:
            phone = 'Неизвестно'
        prodeject_list.append(
            {
                'Кто требуется': vakansia,
                'Зарплата': zarplata,
                'Номер телефона': phone,
                'Ссылка':url
            }
        )
        with open('project_orsk_ru.json', 'a', encoding="utf-8") as file:
            json.dump(prodeject_list, file, indent=4, ensure_ascii=False)
    time.sleep(random.randrange(2, 3))