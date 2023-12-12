from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from transliterate import translit


def my_slugify(text):
    return slugify(translit(text, 'ru', reversed=True))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=TradeLogistic.Status.PUBLISHED)


class TradeLogistic(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    class Meta:
        verbose_name = 'Торговая логистика'
        verbose_name_plural = 'Торговая логистика'
        ordering = ['time_create']  # для обратного эффекта поставить '-'
        indexes = [models.Index(fields=['-time_create'])]

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг',
                            validators=[
                                MinLengthValidator(5, 'Минимум 5 символов'),
                                MaxLengthValidator(100, 'Максимум 100 символов')
                            ])
    content = models.TextField(blank=True, verbose_name='Содержание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISHED, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории')
    tags = models.ManyToManyField('TagPost', related_name='tags', verbose_name='Теги')
    note = models.OneToOneField('Note', on_delete=models.SET_NULL, null=True, blank=True, related_name='post',
                                verbose_name='Примечание')
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = my_slugify(self.title)
        super().save(*args, **kwargs)


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100, db_index=True, verbose_name='Категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    objects = models.Manager()

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Note(models.Model):
    class Meta:
        verbose_name = 'Примечание'
        verbose_name_plural = 'Примечания'

    name = models.CharField(max_length=100, verbose_name='Описание')
    readiness = models.IntegerField(null=True, verbose_name='Готовность')
    priority = models.IntegerField(blank=True, default=0, verbose_name='Приоритет')
    objects = models.Manager()

    def __str__(self):
        return self.name


class DocumentInfo(models.Model):
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    date_placement = models.DateField(blank=False, verbose_name='Дата')
    num_item = models.CharField(max_length=30, unique=True, null=True, db_index=True, verbose_name='№ УВР')
    num_transport = models.CharField(max_length=255, blank=False, null=True, db_index=True, verbose_name='№ авто')
    num_doc = models.CharField(max_length=255, blank=False, null=True, verbose_name='№ документов')
    date_docs = models.CharField(max_length=255, blank=False, null=True, verbose_name='Дата доков')
    documents = models.CharField(max_length=255, blank=False, null=True, verbose_name='Документы')
    status = models.CharField(max_length=255, blank=False, null=True, verbose_name='Статус УВР')
    num_nine = models.CharField(max_length=30, blank=False, null=True, verbose_name='№ Длинной "9"')
    num_td = models.CharField(max_length=50, blank=False, null=True, verbose_name='Таможенное разрешение')
    path_doc = models.CharField(max_length=255, blank=False, null=True, verbose_name='Путь')
    objects = models.Manager()

    def __str__(self):
        return self.num_item

