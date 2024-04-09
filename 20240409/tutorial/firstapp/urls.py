from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('01_html/', views.htmlview01)
]
