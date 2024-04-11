from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('01_html/', views.htmlView01),
    path('02_link/', views.linkView),
    path('03_css/', views.cssView03),
    path('04_css/', views.cssView04),
    path('05_css/', views.cssView05),
    path('06_css/', views.cssView06),
    path('07_table/', views.tableView07),
    path('08_table/', views.tableView08),
    path('09_table/', views.tableView09),
]
