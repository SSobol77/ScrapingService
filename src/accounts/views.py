import datetime as dt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, \
    ContactForm
from scraping.models import Error

User = get_user_model()

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    messages.success(request, 'Вы успешно вошли в систему!')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь успешно добавлен в систему!')
        return render(request, 'accounts/register_done.html',
                      {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные успешно сохранены!')
                return redirect('accounts:update')

        form = UserUpdateForm(
            initial={'city': user.city, 'language': user.language,
                     'send_email': user.send_email})
        return render(request, 'accounts/update.html',
                      {'form': form, 'contact_form': contact_form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удален!')
    return redirect('home')
def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'email': email, 'language': language})
                err.data['user_data'] = data
                err.save()
            else:
                data = {'user_data': [
                    {'city': city, 'email': email, 'language': language}
                ]}
                Error(data=data).save()
            messages.success(request, 'Данные отправлены Админу SOHO*AI')
            return redirect('accounts:update')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')































User = get_user_model()

# Create your views here.
# https://docs.djangoproject.com/en/3.2/topics/auth/default/#how-to-log-a-user-in
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        messages.success(request, 'Приветствуем тебя в системе SohoAI !')
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


# https://docs.djangoproject.com/en/3.2/topics/auth/default/#django.contrib.auth.logout
def logout_view(request):
    logout(request)
    return redirect('home')


# account register UserRegistrationForm
def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь успешно добавлен в систему')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


# UserUpdateForm
def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                # user.date_of_birth = data['date_of_birth']
                user.save()
                messages.success(request, 'Изменения добавлены в систему')
                return redirect('accounts:update')
        else:
            form = UserUpdateForm(
                initial={'city': user.city, 'language': user.language,
                        'send_email': user.send_email}) #'date_of_birth': user.date_of_birth
            return render(request, 'accounts/update.html', {'form': form})
    else:
        return redirect('accounts:login')


# Удаление установок Usera:
def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удалён!')
    return redirect('home')
