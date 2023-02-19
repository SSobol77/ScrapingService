import os, sys
import django
import datetime
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from scraping.models import Vacancies, Error, Url
from ScrapingService.settings import (
    EMAIL_HOST_USER,
    EMAIL_HOST, EMAIL_HOST_PASSWORD
)



#  Устанавливаем абсолютный путь для DJANGO к проекту, т.к. на машине разработчика и на сервере
#  где будет заинсталлировано разные пути и папки:
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "ScrapingService.settings"

django.setup()  # запуск Django !!!!!!!!!!!!!!!


ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()  # точка - дата отправки письма клиенту
subject = f"Рассылка вакансий за {today}"  # заголовок письма
text_content = f"Рассылка вакансий {today}"  # текстовое значение явно не используется
from_email = EMAIL_HOST_USER   # указываем эмайл с которого будет непосредственно происходить отправка
empty = '<h5> Сегодня обновления отсутствуют.</h5>'


User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(i['email'])
if users_dct:
    params = {'city_id__in': [], 'language_id__in': []} # __in говорит о том что найти все значения принадлежащие этой паре
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancies.objects.filter(**params, timestamp=today).values()[:10]  # ???????????**********
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''  # шаблончик
        for row in rows:   # сформируем текст эмайла
            html += f'<h6"><a href="{ row["url"] }">{ row["title"] }</a></h6>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:   # отправляем эмайл:
            to = email
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to]
            )
            msg.attach_alternative(_html, "text/html")
            msg.send()

# отбор ошибок: _________________________________________________________________________________
qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p"><a href="{ i["url"] }">Error: { i["title"] }</a></p><br>'
    subject += f"Ошибки скрапинга {today}"
    text_content += "Ошибки скрапинга"
    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей </h2>'
        for i in data:
            _html += f'<p">Город: {i["city"]}, Специальность:{i["language"]},  Имейл:{i["email"]}</p><br>'
        subject += f" Пожелания пользователей {today}"
        text_content += "Пожелания пользователей"

qs = Url.objects.all().values('city', 'language')
urls_dct = {(i['city'], i['language']): True for i in qs}
urls_err = ''
for keys in users_dct.keys():  # есть ли ключ из словаря с юзерами в словаре с урлами
    if keys not in urls_dct:
        if keys[0] and keys[1]:
            urls_err += f'<p"> Для города: {keys[0]} и специальности: {keys[1]} отсутствуют urls</p><br>'
if urls_err:
    subject += ' Отсутствующие urls '
    _html += '<hr>'
    _html += '<h5>Отсутствующие urls</h5>'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()


# #------------------------------------------------------------------------------------------------
# qs = Error.objects.filter(timestamp=today)
# if qs.exists():
#     error = qs.first()
#     data = error.data
#     _html = ''
#     for i in data:
#         _html += f'<p><a href="{i["url"]}">Error: {i["title"]}</a></p>'
#     subject = f"Ошибки скрапинга {today}"
#     text_content = f"Ошибки скрапинга"
#     to = ADMIN_USER
#     msg = EmailMultiAlternatives(
#         subject, text_content, from_email, [to]
#     )
#     msg.attach_alternative(_html, "text/html")
#     msg.send()

# Альтернативный метод с помощью библиотеки smtplib, как альтернатива email-Django:

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# msg = MIMEMultipart('alternative')
# msg['Subject'] = 'Список вакансий за  {}'.format(today)
# msg['From'] = EMAIL_HOST_USER
# mail = smtplib.SMTP()
# mail.connect(EMAIL_HOST, 25)
# mail.ehlo()
# mail.starttls()
# mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#
# html_m = "<h1>Hello world</h1>"
# part = MIMEText(html_m, 'html')
# msg.attach(part)
# mail.sendmail(EMAIL_HOST_USER, [to], msg.as_string())
# mail.quit()