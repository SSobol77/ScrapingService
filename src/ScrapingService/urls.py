"""ScrapingService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from scraping.views import home_view, list_view, v_detail, VDetail, VList, VCreate, VUpdate, VDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', list_view, name='list'),  # Django по имени будет создавать относительные ссылки которые можно вставлять в шаблоны
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('detail/<int:pk>/', VDetail.as_view(), name='detail'),
    path('create/', VCreate.as_view(), name='create'),
    path('update/<int:pk>/', VUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', VDelete.as_view(), name='delete'),
    path('', home_view, name='home'),  # привязываем страницу home.html с отображений на ней функции home_view из
    # view.py из базы существующих в ней вакансий
]
