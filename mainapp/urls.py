from django.urls import path

import mainapp.views as mainapp

from .apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", mainapp.products, name="index"),
    path("products/<int:pk>/", mainapp.products, name="products"),
    path("products/<int:pk>/page/<int:page>", mainapp.products, name="page"),
    path("product/<int:pk>/", mainapp.product, name="product"),
    path('catalog/', mainapp.catalog, name='catalog'),
    path('contacts/', mainapp.contacts, name='contacts'),
]