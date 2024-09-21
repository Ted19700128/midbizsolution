#!-- D:/web/midbizsolution/pfcstandard/urls.py

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_pfcs, name='create_pfcs'),
    path('menu/', views.pfcs_menu, name='pfcs_menu'),
    path('detail/<int:document_id>/', views.pfcs_detail, name='pfcs_detail'),
    path('update/<int:document_id>/', views.update_pfcs, name='update_pfcs'),
    path('delete/<int:document_id>/', views.delete_pfcs, name='delete_pfcs'), 
    path('searchpopup/', views.show_search_popup, name='show_search_popup'),       
]
