from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import DataForm, UserForm, QuestionForm, MailForm, PasswordForm, SupportForm
from django.contrib.auth.models import User
from .models import UserUpgrade, SupportModel
from django.contrib import auth
import requests

# Не забудьте поменять
host = 'http://127.0.0.1:8000/' # адресс сервера с сайтом, проверь дабавлен ли он в ALLOWED_HOSTS
req = 'http://84.201.179.230:8000/' # адресс сервера с нейросетью


def main_page(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['error']
            question = question.encode("utf-8")
            response = requests.post(req, data=question)
            result = response.text
        else:
            result = 'Error'
    else:
        form = DataForm()
        result = ''
    return render(request, 'main/index.html', {'result': result, 'form': form})


def about(request):
    return render(request, 'main/about.html')


def profile(request):
    return render(request, 'main/profile.html')


def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            password = form.cleaned_data.get("password")
            mail = form.cleaned_data.get("mail")
            for user in User.objects.all():
                if user.username == name:
                    error = "Данное имя пользователя уже используется"
                    return render(request, 'main/regis.html', {'form': form, 'error': error})
                if user.email == mail:
                    error = "Данная почта уже используется"
                    return render(request, 'main/regis.html', {'form': form, 'error': error})
            user = User.objects.create_user(name, mail, password)
            user.save()
            for model in UserUpgrade.objects.all():
                if model.user == user:
                    model.question = form.cleaned_data['question']
                    model.answer = form.cleaned_data['answer']
                    model.save()
                    break
        return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserForm()
        error = ''
    return render(request, 'main/regis.html', {'form': form, 'error': error})


def reset(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            k = 0
            for user in User.objects.all():
                if user.email == mail:
                    return redirect(str(mail))
                else:
                    k += 1
            if k == len(User.objects.all()):
                error = "Вы не зарегистрированы"
    else:
        form = MailForm()
        error = ''
    return render(request, 'main/reset.html', {'form': form, 'error': error})


def reset_2(request, mail):
    for user in User.objects.all():
        if user.email == mail:
            use = user
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            models = UserUpgrade.objects.all()
            for model in models:
                if model.user == use:
                    ans = model.answer
                    ques = model.question
                    break
            if ans == form.cleaned_data['answer']:
                auth.login(request, use)
                return redirect(str(host) + 'password-change/')
            else:
                error = "Неправильный ответ"
    else:
        models = UserUpgrade.objects.all()
        for model in models:
            if model.user == use:
                ques = model.question
                form = QuestionForm()
        error = ''
    return render(request, 'main/reset_2.html', {'form': form, 'ques': ques, 'error': error})


def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(host)
    else:
        form = PasswordForm()
    return render(request, 'main/change_password.html', {'form': form})


def support(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            SupportModel.objects.create(user=request.user, text=form.cleaned_data['text'])
            return redirect(host)
    else:
        form = SupportForm()
    return render(request, 'main/support.html', {'form': form})
