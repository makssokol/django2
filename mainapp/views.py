from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import datetime
from .models import Contact, ArtObject, ArtCategory
from basketapp.models import Basket
import random
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.template import loader
from django.http import JsonResponse

# Create your views here.


def main(request):
    title = "Art Gallery Flame Art"
    context = {"title": title}
    return render(request, "mainapp/index.html", context)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = get_products()
    return random.sample(list(products), 1)[0]


def products(request, pk=None, page=1):
    title = "Art Objects"
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    if pk is not None:
        if pk == 0:
            products = get_products_ordered_by_price()
            category = {"pk": 0, "name": "all"}
        else:
            category = get_category(pk)
            products = get_products_ordered_by_price()
        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        content = {
            "title": title,
            "products": products_paginator,
            "category": category,
            "media_url": settings.MEDIA_URL,
        }
        return render(request, "mainapp/products_list.html", content)
    products = get_products()[:3]
    content = {
        "title": title,
        "products": products,
        "media_url": settings.MEDIA_URL,
    }
    if pk:
        print(f"User select category: {pk}")
    return render(request, "mainapp/products.html", content)


@cache_page(3600)
def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        title = "Art Objects"
        if request.user.is_authenticated:
            basket = Basket.objects.filter(user=request.user)
        if pk is not None:
            if pk == 0:
                products = get_products_ordered_by_price()
                category = {"pk": 0, "name": "all"}
            else:
                category = get_category(pk)
                products = get_products_ordered_by_price()
            paginator = Paginator(products, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)
            content = {
                "title": title,
                "products": products_paginator,
                "category": category,
                "media_url": settings.MEDIA_URL,
            }
            return render(request, "mainapp/products_list.html", content)
        products = get_products()[:3]
        content = {
            "title": title,
            "products": products,
            "media_url": settings.MEDIA_URL,
        }
        page_content = loader.render_to_string(
            "mainapp/products.html", content, request=request
            )
        return JsonResponse({
            'page_content': page_content
        })

def contacts(request):
    title = "About us"
    visit_date = timezone.now()
    locations = Contact.objects.all()
    content = {
        "title": title,
        "visit_date": visit_date,
        "locations": locations
    }
    return render(request, "mainapp/contacts.html", content)

@cache_page(3600)
def catalog(request):
    title = "Catalog"
    links_menu = get_links_menu()
    hot_product = get_hot_product()
    content = {
        "title": title,
        "links_menu": links_menu,
        "hot_product": hot_product,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "mainapp/catalog.html", content)


def product(request, pk):
    title = "Art Objects"
    content = {
        "title": title,
        "product": get_product(pk),
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "mainapp/product.html", content)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ArtCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ArtCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ArtCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ArtCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = ArtObject.objects.filter(is_active=True,
                                                category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return ArtObject.objects.filter(is_active=True,
                                        category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(ArtObject, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(ArtObject, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = ArtObject.objects.filter(is_active=True,
                                                category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return ArtObject.objects.filter(is_active=True,
                                        category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = ArtObject.objects.filter(category__pk=pk, is_active=True,
                                                category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return ArtObject.objects.filter(category__pk=pk, is_active=True,
                                        category__is_active=True).order_by('price')
