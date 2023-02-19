from django import forms

from scraping.models import City, Language, Vacancies



# формы

# поисковик Search:
class SearchForms(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="slug", required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Город'
    )
    # добавляем атрибут widget, который позволяет прокинуть какие-либо дополнительные атрибуты в виде классов для оформления инпутов
    # добавляем чтобы City и Language не брались с названия поля 

    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name="slug", required=False,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность'
    )

class VForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Город'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Специальность'
    )
    url = forms.CharField(label='URL', widget=forms.URLInput(
        attrs={'class': 'form-control'}))
    title = forms.CharField(label='Заголовок вакансии', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    company = forms.CharField(label='Компания', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание вакансии',
                                  widget=forms.Textarea(
                                      attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancies
        fields = '__all__'
