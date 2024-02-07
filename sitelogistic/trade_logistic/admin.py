from django.contrib import admin, messages
from django import forms
from django.http import HttpResponseRedirect

from admin_extra_buttons.api import ExtraButtonsMixin, button
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from trade_logistic.external_utils.connecter_fdb import *
from .models import *
from .scheduler import start_scheduler, stop_scheduler


class NoteFilter(admin.SimpleListFilter):
    title = 'Статус модуля'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('noted', 'С примечанием'),
            ('empty', 'Не заполнены')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'noted':
            return queryset.filter(note__isnull=False)
        elif self.value() == 'empty':
            return queryset.filter(note__isnull=True)


class PostsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        models = TradeLogistic
        fields = '__all__'


@admin.register(TradeLogistic)
class TradeLogisticAdmin(admin.ModelAdmin):
    form = PostsAdminForm
    fields = ['title', 'slug', 'content', 'cat', 'note', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [NoteFilter, 'cat__name', 'is_published']

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, trade_logistic: TradeLogistic):
        return f'Описание {len(trade_logistic.content)} символов.'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=TradeLogistic.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей.')

    @admin.action(description='Убрать из публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=TradeLogistic.Status.DRAFT)
        self.message_user(request, f'{count} записей сняты с публикации!', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TagPost)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug',)
    list_display_links = ('id', 'tag', 'slug',)
    prepopulated_fields = {'slug': ('tag',)}


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'readiness', 'readiness', 'priority',)
    list_display_links = ('id', 'name', 'readiness', 'readiness', 'priority',)


@admin.register(PDFDataBase)
class PDFDataBaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PDFDataBase._meta.fields]
    list_display_links = ('id',)


@admin.register(DocumentInfo)
class DocumentInfoAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = [field.name for field in DocumentInfo._meta.get_fields()]
    list_display_links = ('id', 'num_item',)

    @button(
        label='Загрузить данные',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def load_data(self, request):
        records = get_data_fdb(HOSTNAME, DATABASE_PATH, USERNAME, PASSWORD)
        for record in records:
            if not DocumentInfo.objects.filter(num_item=record[0]).exists():
                DocumentInfo.objects.create(
                    date_placement=record[1],
                    num_item=record[0],
                    num_transport=record[3].replace(';', '; '),
                    num_doc=record[4],
                    date_docs=record[7],
                    documents=record[6],
                    status=record[9],
                    num_nine=record[10],
                    num_td=record[11] if record[11] is None else record[11][:30].replace(';', '; ')
                )

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @button(
        label='Запустить планировщик',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def admin_start_scheduler(self, request):
        start_scheduler()

    @button(
        label='Остановить планировщик',
        change_form=True,
        html_attrs={"class": 'btn-primary'}
    )
    def admin_stop_scheduler(self, request):
        stop_scheduler()
    # @button(
    #     label='Найти pdf',
    #     change_form=True,
    #     html_attrs={"class": 'btn-primary'}
    # )
    # def match_docs_pdf(self, request):
    #
    #     pdf_dict = list_files(PDFS_CATALOG_PATH)
    #
    #     for num, path in pdf_dict.items():
    #         pass
    #         try:
    #             record = DocumentInfo.objects.get(num_item=num)
    #             record.path_doc = path
    #             record.save()
    #         except ObjectDoesNotExist:
    #             print("Запись не найдена")
