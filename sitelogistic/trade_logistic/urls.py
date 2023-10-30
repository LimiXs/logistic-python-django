from django.urls import path, re_path, register_converter
from . import views
from . import converters
from .views import *

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    # path('', views.index, name='home'),
    path('', TradeLogisticHome.as_view(), name='home'),
    path('about', views.about, name='about'),
    path('get-exel', views.getexcel, name='getexcel'),
    path('add-page', views.addpage, name='addpage'),
    path('contact', views.contact, name='contact'),
    path('upload-file', views.uploadfile, name='uploadfile'),
    path('login', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', TradeLogisticCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag')
]
