import requests
import codecs  # с ее помощью меняем кракозябры на слова
from bs4 import BeautifulSoup as BS  # импортируем чтобы вытянуть из реьд нужное, as BS добавили чтобы длинно не писать

# представимся мозиллой
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }



# url = 'https://www.praca.pl/informatyka-programowanie.html'

'''work.ua'''
# создаем функцию для этого домена work.ua, который будем скрабить :
def work(url):
    # создадим два списка-массива в которых будем хранить отдельно нормальную информацию jobs и ошибки errors:
    # создадим переменную jobs как список, в которую будем сохранять словари для дальшего занесения в базу:
    jobs = []
    # создадим переменную errors как список в котором будем собирать информацию для последующей ручной обработки:
    errors = []
    # адрес который будем скрабить:
    domain = 'https://www.work.ua'
    url = 'https://www.work.ua/ru/jobs-kyiv-python/'

    # отправляем библиотеку рекуэст в качестве запроса:
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:  # проверяем если вернулся запрос с сервера полный то 200
        soup = BS(resp.content, 'html.parser')  # создаем суп из html обязательно указываем тип parser
        # из супа достаем div с параметром id= которому присваиваем 'pjax-job-list' , копируя с кода страницы:
        main_div = soup.find('div', id='pjax-job-list')
        if main_div:  # проверяем main_div
            # передаем как параметры атрибуты по которым будем искать, названия их берем со страницы:
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            # теперь обрабатываем найденный список циклом:
            for div in div_list:
                title = div.find(
                    'h2')  # title это объект BS, а find применяем т.к. <h2> ваступает только один раз в нужном коде
                href = title.a[
                    'href']  # тэг <a>  - это подчиненный класс h2, так получаем ссылку url, которую здесь назвали 'href='
                content = div.p.text  # получаем контэнт орисание из тэга <p>
                company = 'No name'  # название может отсутствовать, тогда ищем картику лога
                logo = div.find('img')
                if logo:
                    company = logo['alt']  # если находит, то считывает текст из тега alt=
                # теперь добавим все эти значения в виде словарей в job в базу данных, они должны совпадать
                # с названиями из accounts\modeles.py , значение title.text в таком виде, т.к. сам title это объект, а нам нужно его поле:
                jobs.append({'title': title.text, 'url': domain + href, "description": content, 'company': company})
                # добавляем в список-массив ошибки с соотв. комментариями:
            else: errors.append({'url': url, 'title': "Div does not exists"})  # поменялся id и отсутствует div
        else:
            errors.append({'url': url, 'title': "Page do not response"})  # отсутствует страница

        return jobs, errors



'''rabota.ua'''
# создаем функцию для этого домена rabota.ua, который будем скрабить. В отличии от предыдущего будем скрабить таблицы
# вместо div:
def rabota(url):
    # создадим два списка-массива в которых будем хранить отдельно нормальную информацию jobs и ошибки errors:
    # создадим переменную jobs как список, в которую будем сохранять словари для дальшего занесения в базу:
    jobs = []
    # создадим переменную errors как список в котором будем собирать информацию для последующей ручной обработки:
    errors = []

    # адрес который будем скрабить:
    domain = 'https://rabota.ua'

    # отправляем библиотеку рекуэст в качестве запроса:
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:  # проверяем если вернулся запрос с сервера полный то 200
        soup = BS(resp.content, 'html.parser')  # создаем суп из html обязательно указываем тип parser

        # из супа достаем table с параметром id= которому присваиваем 'ctl00_content_vacancylist_gridList',
        # копируя это название идинтификатора из кода страницы:
        mainDiv = soup.find('div', id='_ngcontent-app-desktop-c228')
        if mainDiv:  # проверяем main_div
            # передаем как параметры атрибуты по которым будем искать все tr, названия их берем со страницы:
            div_lst= mainDiv.find_all('div', attrs={'class': 'ng-tns-c221-46'})  # т.е. будет происходить поиск для всех tr у которых id есть
            # теперь обрабатываем найденный список циклом:
            for div in div_lst:
                div= div_lst.find('div', attrs={'class': 'ng-tns-c221-46'})  # ищем div у которого атрибуты class называются card-body
                if div:  # проверка если div существует, чтобы обойти рекламы в этой части контекста страницы между таблицами
                    title = div.find('h2')  # ищем <h2> у которого class с атрибутом card-title
                    href = title.a['href']  # тэг <a>  - это подчиненный класс h2, так получаем ссылку url, которую здесь назвали 'href='
                    content = div.p.text  # получаем контэнт орисание из тэга <p>
                    company = 'No name'  # название может отсутствовать, тогда ищем картику лога
                    p = div.find('div', attrs={'class': 'company-name'})
                    if p:
                        company = p.a.text  # если <p> находит, то считывает текст из тега <a>, который внутри <p>

                    # теперь добавим все эти значения в виде словарей в job в базу данных, они должны совпадать
                    # с названиями из accounts\modeles.py , значение title.text в таком виде, т.к. сам title это объект, а нам нужно его поле:
                    jobs.append({'title': title.text, 'url': domain + href, "description": content, 'company': company})

                # добавляем в список-массив ошибки с соотв. комментариями:

            else:
                errors.append({'url': url, 'title': "Table does not exists"})  # поменялся id и отсутствует таблица
        else:
            errors.append({'url': url, 'title': "Page do not response"})  # отсутствует страница

        return jobs, errors


if __name__=='__main__':
    url = 'https://rabota.ua/ua/zapros/%25D0%25BF%25D1%2580%25D0%25BE%25D0%25B3%25D1%2580%25D0%25B0%25D0%25BC%25D0%25BC%25D0%25B8%25D1%2581%25D1%2582-python/%D0%BA%D0%B8%D0%B5%D0%B2'
    jobs, errors = rabota(url)
    # открываем файл в формате json или txt в режиме записи
    h = codecs.open('work.txt', 'w', 'utf-8')
    # записываем полученные данные в байтах т.е. переопределяем их:
    h.write(str(jobs))
    # закрываем хендер:
    h.close()