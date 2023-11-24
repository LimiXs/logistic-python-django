import os
import pandas as pd
import csv
from io import TextIOWrapper

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import AuthenticationForm
# from django.core.paginator import Paginator
# from django.template.loader import render_to_string
from .forms import *
from .models import *
from .utils import *
from trade_logistic.external_utils.connecter_fdb import *


class TradeLogisticHome(DataMixin, ListView):
    model = TradeLogistic
    template_name = 'trade_logistic/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return TradeLogistic.objects.filter(is_published=True)


class TradeLogisticCategory(DataMixin, ListView):
    model = TradeLogistic
    template_name = 'trade_logistic/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Разделы - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return TradeLogistic.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


class ShowPost(DataMixin, DetailView):
    model = TradeLogistic
    template_name = 'trade_logistic/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'trade_logistic/add_page.html'
    success_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


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


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=TradeLogistic.Status.PUBLISHED).select_related('cat')
    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'trade_logistic/index.html', context=data)


def handle_uploaded_file(file):
    data = []
    reader = csv.reader(TextIOWrapper(file, encoding='utf-8'), delimiter=';')
    for row in reader:
        data.append(row)
    return data


def upload_file(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        data = handle_uploaded_file(csv_file)
        return render(request, 'trade_logistic/display_csv.html', {'data': data})

    return render(request, 'trade_logistic/upload_file.html')


def get_excel(request):
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


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def about(request):
    if request.method == 'POST':
        pass
    return render(request, 'trade_logistic/about.html', {'title': 'Немного о нас', 'menu': menu})


def contact(request):
    return HttpResponse(f"Обратная связь")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'trade_logistic/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'trade_logistic/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def my_view(request):
    data = DocumentInfo.objects.all()
    return render(request, 'trade_logistic/display_csv.html', {'data': data})


def get_doc_info(request):
    fields = DocumentInfo._meta.get_fields()
    field_names = [field.verbose_name for field in fields]

    data = {
        'menu': menu,
        'fields': field_names
    }
    if request.method == 'POST':
        data['records'] = DocumentInfo.objects.all()

    return render(request, 'trade_logistic/fdb_data.html', context=data)
