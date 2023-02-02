from django.db import models

from scraping.utils import from_cyrillic_to_eng


# Create your models here:


# Создаем модель Город:
class City(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название города',
                            unique=True)
    slug = models.CharField(max_length=50,
                            blank=True,
                            unique=True)

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
    slug = models.CharField(max_length=50,
                            blank=True,
                            unique=True)

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
    title = models.CharField(max_length=300, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=100, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('city', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    # переопределяем метод
    def __str__(self):
        return self.title
