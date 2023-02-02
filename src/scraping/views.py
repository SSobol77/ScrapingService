from django.shortcuts import render

from .forms import SearchForms
from .models import  Vacancies


# функция отображения вакансий на home.html
def home_view(request):
    #print(request.POST) #вывод запроса POST из поиска в консоль
    #print(request.GET) #вывод запроса GET из поиска в консоль

    form = SearchForms()  # объявляем нашу форму поиска и импортируем SearchForms из forms.py

    city = request.GET.get('city')  # получаем данные запроса города из словаря в функцию
    language = request.GET.get('language')  # получаем данные запроса языка прогр. из словаря в функцию


    # проверяем заполненены ли поля Поиска:
    qs = []   # queryset определяем пустым изначально в поисковике
    if city or language:
        _filter = {}  # фильтруем по словарю
        if city:
            _filter['city__slug'] = city  #двойное подчеркивание значит ищем в базе таблице City по имени Name но slug
        if language:
            _filter['language__slug'] = language  # ищем в базе таблице Language по имени Name но slug (маленькими буквами и т.д)

        qs = Vacancies.objects.filter(**_filter)  # делаем запрос к базе данных, чтобы раскрыть словарь и получить все нужные записи


    # Это рендер для отрисовки:

    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})  # выводим на странице home.html,
# как словарь {'object_list': qs, 'form': form} - полученные данные далее нужно зайти в url, чтобы подвязать адрес
    
