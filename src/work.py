import requests
import codecs # с ее помощью меняем кракозябры на слова
from bs4 import BeautifulSoup as BS  # импортируем чтобы вытянуть из реьд нужное, as BS добавили чтобы длинно не писать

#представимся мозиллой
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

# адрес который будем скрабить:
#url = 'https://www.praca.pl/informatyka-programowanie.html'
domain = 'https://www.work.ua'
url ='https://www.work.ua/ru/jobs-kyiv-python/'

# отправляем библиотеку рекуэст в качестве запроса:
resp = requests.get(url, headers=headers)


# создадим два списка-массива в которых будем хранить отдельно нормальную информацию jobs и ошибки errors:

# создадим переменную jobs как список, в которую будем сохранять словари для дальшего занесения в базу:
jobs =[]
# создадим переменную errors как список в котором будем собирать информацию для последующей ручной обработки:
errors=[]

if resp.status_code==200:     # проверяем если вернулся запрос с сервера полный то 200
    soup = BS(resp.content, 'html.parser')   #создаем суп из html обязательно указываем тип parser

    # из супа достаем div с параметром id= которому присваиваем 'pjax-job-list' , копируя с кода страницы:
    main_div = soup.find('div', id='pjax-job-list')
    if main_div:  # проверяем main_div

        # передаем как параметры атрибуты по которым будем искать, названия их берем со страницы:
        div_list = main_div.find_all('div',attrs={'class':'job-link'})

        # теперь обрабатываем найденный список циклом:
        for div in div_list:
            title=div.find('h2') # title это объект BS, а find применяем т.к. <h2> ваступает только один раз в нужном коде
            href= title.a['href']  # тэг <a>  - это подчиненный класс h2, так получаем ссылку url, которую здесь назвали 'href='
            content=div.p.text  #  получаем контэнт орисание из тэга <p>
            company = 'No name' # название может отсутствовать, тогда ищем картику лога
            logo=div.find('img')
            if logo:
                company = logo['alt'] #если находит, то считывает текст из тега alt=

            # теперь добавим все эти значения в виде словарей в job в базу данных, они должны совпадать
            # с названиями из accounts\modeles.py , значение title.text в таком виде, т.к. сам title это объект, а нам нужно его поле:
            jobs.append({'title':title.text,'url':domain+href,"description":content,'company':company})

        # добавляем в список-массив ошибки с соотв. комментариями:
        else:
            errors.append({'url':url, 'title': "Div does not exists"})  # поменялся id и отсутствует div
    else:
        errors.append({'url':url, 'title': "Page do not response"}) # отсутствует страница

# открываем файл в формате json или txt в режиме записи
h = codecs.open('work.txt', 'w', 'utf-8')

# записываем полученные данные в байтах т.е. переопределяем их:
h.write(str(jobs))
# закрываем хендер:
h.close()



