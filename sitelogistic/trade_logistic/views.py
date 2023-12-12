import os
import pandas as pd
import csv
import django_tables2 as tables
from io import TextIOWrapper

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
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import AuthenticationForm
# from django.core.paginator import Paginator
# from django.template.loader import render_to_string
# from trade_logistic.external_utils.connecter_fdb import *
from .forms import *
from .models import *
from .tables import DocTable, DocsFilter
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


#
# class DocsListView(ListView):
#     model = DocumentInfo
#     # attrs = {'class': 'my-table'}
#     table_class = DocTable
#     template_name = 'trade_logistic/fdb_data.html'
#
#     def download_file(self, request, path):
#         file_path = os.path.join('path_to_your_files_directory', path)  # Путь к файлу
#         print(file_path)
#         if os.path.exists(file_path):
#             with open(file_path, 'rb') as file:
#                 response = FileResponse(file)
#                 return response
#         return None
#
#     def post(self, request, *args, **kwargs):
#         if request.POST.get('method') == 'post':
#             pass
#
#         if 'path' in request.GET:
#             file_response = self.download_file(request, request.GET['path'])
#             if file_response:
#                 return file_response
#
#         return super().post(request, *args, **kwargs)


# def get_doc_info(request):
#     documents = DocumentInfo.objects.all()  # Получаем все объекты DocumentInfo
#     return render(request, 'trade_logistic/fdb_data.html', {'documents': documents})


# def get_doc_info(request):
#     fields = DocumentInfo._meta.get_fields()
#     field_names = [field.name for field in fields if field.name != 'id']
#
#     sort_by = request.GET.get('sort_by')
#     filter_by = request.GET.get('filter_by')  # Получаем параметр для фильтрации
#
#     records = DocumentInfo.objects.all()
#
#     if filter_by:  # Если параметр для фильтрации передан
#         # Создаем Q-объекты для фильтрации по всем полям модели
#         filter_query = Q()
#         for field_name in field_names:
#             filter_query |= Q(**{f"{field_name}__icontains": filter_by})
#
#         records = records.filter(filter_query)
#
#     if sort_by in field_names:
#         records = records.order_by(sort_by)
#
#     data = {
#         'menu': menu,
#         'fields': field_names,
#         'records': records,
#         'current_filter': filter_by  # Передаем текущее значение фильтра в шаблон
#     }
#
#     return render(request, 'trade_logistic/fdb_data.html', context=data) SingleTableView,


class DocsListView(DataMixin, SingleTableMixin, FilterView):
    model = DocumentInfo
    table_class = DocTable
    template_name = 'trade_logistic/fdb_data.html'

    filterset_class = DocsFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))
