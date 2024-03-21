import os
import pandas as pd
import csv
import django_tables2 as tables
from io import TextIOWrapper
import pandas
from django.shortcuts import render
from django.db.models import Q
from django.db.models import F
from django.http import FileResponse
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView, LazyPaginator, RequestConfig
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.urls import include, path

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import AuthenticationForm
# from django.core.paginator import Paginator
# from django.template.loader import render_to_string
# from trade_logistic.external_utils.connecter_fdb import *
from .forms import *
from .models import *
from .tables import DocTable, DocsFilter, ERIPTable, ERIPFilter
from .utils import *


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


class DocsListView(DataMixin, SingleTableMixin, FilterView):
    model = DocumentInfo
    table_class = DocTable
    template_name = 'trade_logistic/fdb_data.html'
    filterset_class = DocsFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'].paginate = False  # Отключаем автоматическую пагинацию
        return dict(list(context.items()))


def download(request, path_doc):
    file_path = path_doc
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'
    return response


def show_happy_birthdays(request):
    TXT_FILE = r'D:\khomich\static_sitelogistic\happy_birthdays_bts.txt'
    with open(TXT_FILE, 'r', encoding='utf-8') as file:
        for _ in range(9):  # Пропускаем первые 9 строк
            next(file)

        df = pd.read_csv(file, delimiter='\t', names=['ФИО (полное)', 'Должность', 'Подразделение', 'Дата рождения', 'Возраст'])

    df['Дата рождения'] = pd.to_datetime(df['Дата рождения'], format='%d.%m.%Y')
    now = pd.Timestamp('now')
    df['days_until_birthday'] = (df['Дата рождения'].dt.month - now.month)*30 + df['Дата рождения'].dt.day - now.day
    df.loc[df['days_until_birthday'] < 0, 'days_until_birthday'] += 360
    df = df.sort_values(by='days_until_birthday')

    df = df.drop_duplicates(subset='ФИО (полное)', keep='first')
    df = df.head(20)
    df = df.drop(columns=['days_until_birthday'])

    df['Дата рождения'] = df['Дата рождения'].dt.strftime('%d.%m.%Y')

    html_table = df.to_html()

    return render(
        request,
        'trade_logistic/happy_birthdays.html',
        {'data': html_table}
    )


def erip_info(request):
    erip_filter = ERIPFilter(request.GET, queryset=ERIPDataBase.objects.all())
    table = ERIPTable(erip_filter.qs)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)
    return render(request, 'trade_logistic/erip_info.html', {'table': table, 'filter': erip_filter})
