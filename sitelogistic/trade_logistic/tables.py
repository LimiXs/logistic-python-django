import django_tables2 as tables
from .models import DocumentInfo
from django_filters import FilterSet


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
    class Meta:
        model = DocumentInfo
        fields = {"date_placement": ["contains"], "num_item": ["contains"]}
