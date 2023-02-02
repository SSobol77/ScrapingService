from django import forms

from scraping.models import City, Language


# формы

# поисковик Search:
class SearchForms(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name= 'slug', required= False,
                                  widget=forms.Select(attrs={'class':'form-control'}),
                                  label='Город')
    # добавляем атрибут widget, который позволяет прокинуть какие-либо дополнительные атрибуты в виде классов для оформления инпутов
    # добавляем чтобы City и Language не брались с названия поля 

    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label='Язык програм.')
