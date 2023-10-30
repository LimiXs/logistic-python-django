import os
from io import TextIOWrapper

import pandas as pd
import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.generic import ListView

from .forms import *
from .models import *

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Получить шаблон', 'url_name': 'getexcel'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Загрузить инвойс', 'url_name': 'uploadfile'},
    {'title': 'Войти', 'url_name': 'login'}
]


def about(request):
    if request.method == 'POST':
        pass
    return render(request, 'trade_logistic/about.html', {'title': 'О сайте', 'menu': menu})


def getexcel(request):
    cap = {
        '№': [], 'Код товара': [], 'Наименование': [], 'Артикул': [], 'Торговая марка': [], 'Производитель': [],
        'Страна': [], 'Ед. изм.': [], 'Кол-во в ед. изм.': [], 'Цена': [], 'Стоимость': [],
        'Вес  нетто': [], 'Вес  брутто': [], 'Доп. код': []
    }
    df = pd.DataFrame(cap)
    pd.set_option('display.colheader_justify', 'center')

    excel_file_path = 'invoice_template.xlsx'
    df.to_excel(excel_file_path, index=False)

    with open(excel_file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(excel_file_path)}'

    return response


# print(form.cleaned_data)
def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # try:
            #     TradeLogistic.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except:
            #     form.add_error(None, 'Ошибка добавления поста')
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'trade_logistic/addpage.html', data)


def show_post(request, post_slug):
    post = get_object_or_404(TradeLogistic, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'trade_logistic/post.html', data)


def contact(request):
    return HttpResponse(f"Обратная связь")


def handle_uploaded_file(file):
    # Обработка загруженного файла
    data = []
    # Парсинг CSV и добавление данных в список
    reader = csv.reader(TextIOWrapper(file, encoding='cp1251'), delimiter=';')
    for row in reader:
        data.append(row)
    return data


def uploadfile(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        data = handle_uploaded_file(csv_file)
        return render(request, 'trade_logistic/display_csv.html', {'data': data})

    return render(request, 'trade_logistic/uploadfile.html')


def login(request):
    return HttpResponse(f"Авторизация")


class TradeLogisticHome(ListView):
    model = TradeLogistic
    template_name = 'trade_logistic/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return TradeLogistic.objects.filter(is_published=True)


class TradeLogisticCategory(ListView):
    model = TradeLogistic
    template_name = 'trade_logistic/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return TradeLogistic.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

# def index(request):
#     posts = TradeLogistic.published.all().select_related('cat')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0
#     }
#     return render(request, 'trade_logistic/index.html', context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = TradeLogistic.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Модуль: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk
    }
    return render(request, 'trade_logistic/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=TradeLogistic.Status.PUBLISHED).select_related('cat')
    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'trade_logistic/index.html', context=data)
