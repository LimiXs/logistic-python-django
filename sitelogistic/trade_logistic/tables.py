import django_tables2 as tables
from django import forms
from .models import DocumentInfo, ERIPDataBase
from django_filters import FilterSet, CharFilter, DateFromToRangeFilter


class DocTable(tables.Table):
    class Meta:
        model = DocumentInfo
        attrs = {'class': 'table table-sm'}
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'date_placement',
            'num_item',
            'num_transport',
            'num_doc',
            'date_docs',
            'documents',
            'status',
            'num_nine',
            'num_td',
        )

    download = tables.TemplateColumn(
        verbose_name='Путь/Кнопка',
        template_name='trade_logistic/download_button.html',
        visible=True,
        order_by=('path_doc',)
    )


class DocsFilter(FilterSet):
    # date_placement = DateFromToRangeFilter(
    #     widget=forms.DateInput(attrs={'class': 'datepicker'})
    # )

    class Meta:
        model = DocumentInfo
        fields = {"num_item": ["contains"], "date_placement": ["contains"]}


class ERIPTable(tables.Table):
    class Meta:
        model = ERIPDataBase
        attrs = {'class': 'table table-sm'}
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'id_account',
            'payer_name',
            'bill_pay',
            'date',
        )
        show_footer = False


class ERIPFilter(FilterSet):
    id_account = CharFilter(field_name='id_account', lookup_expr='icontains', label='Счёт договора')
    payer_name = CharFilter(field_name='payer_name', lookup_expr='icontains', label='ФИО плательщика')
    date = DateFromToRangeFilter(label='Дата оплаты')

    class Meta:
        model = ERIPDataBase
        fields = ['id_account', 'payer_name', 'date']
