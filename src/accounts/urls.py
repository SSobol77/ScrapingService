from django.urls import path
from accounts.views import (
    login_view, logout_view, register_view, update_view, delete_view, contact
)


# Django по имени будет создавать относительные ссылки которые можно вставлять в шаблоны
urlpatterns = [
    path('login/', login_view, name='login'),   # привязываем страницу с отображений на ней функции login_view
    path('logout/', logout_view, name='logout'),  # привязываем страницу с отображений на ней функции logout_view
    path('register/', register_view, name='register'),  # def register_view
    path('update/', update_view, name='update'),  # def update_view -- user settings
    path('delete/', delete_view, name='delete'),  # def delete_view - delete settings
    path('contact/', contact, name='contact'),
]



