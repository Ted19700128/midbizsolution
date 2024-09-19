#!-- D:/web/midbizsolution/pfcstandard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_pfcs, name='create_pfcs'),
    path('searchpopup/', views.show_search_popup, name='show_search_popup'),
]