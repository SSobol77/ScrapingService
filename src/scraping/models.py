import jsonfield
from django.db import models

from scraping.utils import from_cyrillic_to_eng


# Создаю дефаулт функцию для Urls:
def default_urls():
    # возвращаю словарь где прописываю все ключи:
    return {"work": "", "rabota": "", "dou": "", "djinni": ""}


# Создаем здесь наши модели:
# Создаем модель Город:
class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название города', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Название города'
        verbose_name_plural = 'Названия населенных пунктов'

    # переопределяем метод
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)



# Создаем модель Язык программирования:
class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Язык программирования',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)

# Создаем модель Вакансии:
class Vacancies(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город', related_name='vacancies')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):  # переопределяем метод
        return self.title

# Создаем модель Error для сохранения ошибок:
class Error(models.Model):  # наследуемся от models.Model
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    class Meta:
        verbose_name = 'Ошибку'
        verbose_name_plural = 'Ошибки'

    def __str__(self):
        return str(self.timestamp)

# Создадим модель в которой будут храниться адреса пар язык програм. и город
class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "language") # чтобы избежать случайного вписвния или дублирования делаем уникальными сочетания, после этого добавляния
            # мы не сможем вписать уникального сочетания больше чем одна строка: