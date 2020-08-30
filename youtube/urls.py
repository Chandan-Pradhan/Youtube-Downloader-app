from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name="home"),
    path('add_links/', views.add_links, name="add_links"),
    path('download/<int:pl>', views.downloader, name="link_id"),
]