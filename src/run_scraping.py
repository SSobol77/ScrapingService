import codecs
import os, sys


# устанавливаеи абсолютный путь для DJANGO к проекту, т.к. на машине разработчика и на сервере
# где будет заинсталировано разные пути и папки :
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "ScrapingService.settings"
import django
django.setup()  # запуск Django !!!!!!!!!!!!!!!
from sqlite3 import DatabaseError # переносим импорт сюда, т.е. уже после запуска Django


from scraping.parsers import *

from scraping.models import Vacancies, City, Language, Error


# прописываем парсерс фуикций и адресов:
parsers = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D1%97%D0%B2&category=Python'),
    (djinni, 'https://djinni.co/jobs/?primary_keyword=Python&region=UKR&location=kyiv'),
    (rabota, 'https://rabota.ua/ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2')
)

city = City.objects.filter(slug='kiev').first()  # приводим из кварисета к истенсу
language = Language.objects.filter(slug='python').first()   # приводим из кварисета к истенсу

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:

            # поскольку сделано таким образом что ключи в функциях формируются таким же самым образом как
            # и названные имена полей title, url, description и company, то можно здесь раскрыть данный словарь job,
            # причем city и language должны быть указаны явно :
    v = Vacancies(**job, city=city, language=language )
            # для модели вакансий мы установили уникальный url, т.е. существует риск захвата с сайта старых вакансий,
            # если он медленно обнавляется или в выходные дни, т.е. собрать уже имеющиеся в нашей базе вакансии, чтобы их
            # не дублировать, самый эффективный способ это помещение в трай :
    try:
        v.save()  # вакансия сохранится
    except DatabaseError:
        pass
# если появляются ошибки они будут добавлены в список errors и при его наличии запишем его в базуданных :
if errors:
    er = Error(data=errors).save()

#h = codecs.open('work.txt', 'w', 'utf-8')
#h.write(str(jobs))
#h.close()
