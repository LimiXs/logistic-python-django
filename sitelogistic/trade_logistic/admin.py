from django.contrib import admin, messages
from .models import TradeLogistic, Category, TagPost, Note
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


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
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag', 'slug')
    prepopulated_fields = {'slug': ('tag',)}


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'readiness', 'readiness', 'priority')
    list_display_links = ('id', 'name', 'readiness', 'readiness', 'priority')
