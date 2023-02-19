import asyncio
import os, sys
import codecs
import django
import datetime as dt

# устанавливаеи абсолютный путь для DJANGO к проекту, т.к. на машине разработчика и на сервере
# где будет заинсталировано разные пути и папки :
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "ScrapingService.settings"

django.setup()  # запуск Django !!!!!!!!!!!!!!!
from sqlite3 import DatabaseError  # переносим импорт сюда, т.е. уже после запуска Django
from django.db import DatabaseError
from scraping.parsers import *
from scraping.models import Vacancies, Error, Url
from django.contrib.auth import get_user_model

# возвращаем юзера по умолчанию
User = get_user_model()

# прописываем парсерс фуикций и адресов:
parsers = (
    (work, 'work'),
    (dou, 'dou'),
    (djinni, 'djinni'),
    (rabota, 'rabota')
)

jobs, errors = [], []


# функция которая возвращает уникальные наборы города и языка прогр. из Юзера зарегистрированного в системе:
def get_settings():
    qs = User.objects.filter(send_email=True).values()  # values -позволяет получить список словарей, т.е. вместо города и языка получаем их id
    # делаем settings_lst как set потому что может быть несколько пользователей с одинаковыми настройками делаем в виде генератора:
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst  # здесь в settings_lst - храняться настройки по умолчанию для нашего набора значений


# Функция для получения набора урлов (списка словарей), после выбора Юзером набора в виде списка  пары city_id и language_id
def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)


# асинхронный запуск функции скрапинга:
async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]

# for data in url_list:
#
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

if tmp_tasks:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()


for job in jobs:

    # поскольку сделано таким образом что ключи в функциях формируются таким же самым образом как
    # и названные имена полей title, url, description и company, то можно здесь раскрыть данный словарь job,
    # причем city и language будут автоматически прописываться соответственно с тем что ест в моделе вакансии :
    v = Vacancies(**job)
    # для модели вакансий мы установили уникальный url, т.е. существует риск захвата с сайта старых вакансий,
    # если он медленно обнавляется или в выходные дни, т.е. собрать уже имеющиеся в нашей базе вакансии, чтобы их
    # не дублировать, самый эффективный способ это помещение в трай :
    try:
        v.save()  # вакансия сохранится
    except DatabaseError:
        pass
# если появляются ошибки они будут добавлены в список errors и при его наличии запишем его в базуданных :
if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():  # если кто-то написал
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:       # если никто не написал
        er = Error(data=f'errors:{errors}').save()

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
ten_days_ago = dt.date.today() - dt.timedelta(10)
Vacancies.objects.filter(timestamp__lte=ten_days_ago).delete() # выбрать все вакансии которым больше lte чем 10 дней и применить удаление
