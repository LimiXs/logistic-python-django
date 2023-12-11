import django_tables2 as tables
from .models import DocumentInfo


class DocTable(tables.Table):
    template_name = 'django_tables2/bootstrap.html'
    my_column = tables.TemplateColumn(verbose_name=('My Column'),
                                      template_name='app/my_column.html',
                                      orderable=False)  # orderable not sortable

    class Meta:
        model = DocumentInfo
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
            'path_doc'
        )
