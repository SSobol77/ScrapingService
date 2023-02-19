
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, \
    DeleteView

from .forms import SearchForms, VForm
from .models import Vacancies

# функция отображения вакансий на home.html
def home_view(request):
    form = SearchForms()  # объявляем нашу форму поиска и импортируем SearchForms из forms.py
    # Это рендер для отрисовки:
    return render(request, 'scraping/home.html', {'form': form})  # выводим на странице home.html,
            # как словарь {'form': form} - полученные данные далее нужно зайти в url, чтобы подвязать адрес


def list_view(request):
    # print(request.GET)
    form = SearchForms()  # объявляем нашу форму поиска и импортируем SearchForms из forms.py
    city = request.GET.get('city')  # получаем данные запроса города из словаря в функцию
    language = request.GET.get('language')   # получаем данные запроса языка прогр. из словаря в функцию
    # проверяем заполненены ли поля Поиска:
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city   #двойное подчеркивание значит ищем в базе таблице City по имени Name но slug
        if language:
            _filter['language__slug'] = language  # ищем в базе таблице Language по имени Name но slug (маленькими буквами и т.д)

        # делаем запрос к базе данных, чтобы раскрыть словарь и получить все нужные записи:
        qs = Vacancies.objects.filter(**_filter).select_related('city', 'language')
        paginator = Paginator(qs, 5)  # Show 5 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj

        # Это рендер для отрисовки:object_list'
        return render(request, 'scraping/list.html', context)  # выводим на странице list.html,
        # как словарь {'object_list': page_obj, 'form': form} - полученные данные далее нужно зайти в url, чтобы подвязать адрес

def v_detail(request, pk=None):
    # object_ = Vacancies.objects.get(pk=pk)
    object_ = get_object_or_404(Vacancies, pk=pk)
    return render(request, 'scraping/detail.html', {'object': object_})


class VDetail(DetailView):
    queryset = Vacancies.objects.all()
    template_name = 'scraping/detail.html'
    # context_object_name = 'object'


class VList(ListView):
    model = Vacancies
    template_name = 'scraping/list.html'
    form = SearchForms()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form

        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Vacancies.objects.filter(**_filter).select_related('city', 'language')
        return qs


class VCreate(CreateView):
    model = Vacancies
    # fields = '__all__'
    form_class = VForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')


class VUpdate(UpdateView):
    model = Vacancies
    form_class = VForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')



class VDelete(DeleteView):
    model = Vacancies
    # template_name = 'scraping/delete.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
