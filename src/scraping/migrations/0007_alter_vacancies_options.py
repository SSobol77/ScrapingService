# Generated by Django 3.2.16 on 2023-02-12 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0006_alter_url_urls_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancies',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
    ]
