from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from basketapp.models import Basket
from mainapp.models import ArtObject
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import F


@login_required
def basket(request):
    title = "basket"
    basket_items = request.user.basket.select_related(
        'product__category').order_by("product__category")
    content = {
        "title": title,
        "basket_items": basket_items,
        "media_url": settings.MEDIA_URL,
    }
    return render(request, "basketapp/basket.html", content)


@login_required
def basket_add(request, pk):
    if "login" in request.META.get("HTTP_REFERER"):
        return HttpResponseRedirect(reverse("products:product", args=[pk]))
    product = get_object_or_404(ArtObject, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if basket:
        basket.quantity = F('quantity') + 1
    print(f"Product quantity: {product.quantity}")
    print(f"Basket initial: {basket}")

    if not basket:
        print(f'request: {request}, request.user: {request.user}, product: {product}, product.price: {product.price}')
        basket = Basket(user=request.user, product=product, quantity=1)
    print(f"Basket created: {basket}. Basket quantity: {basket.quantity}.")
    print(f"Basket product: {basket.product}.")
    
    basket.save()
    

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_remove(request, pk):
    get_object_or_404(Basket, pk=pk).delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        basket_item = get_object_or_404(Basket, pk=int(pk))
        quantity = int(quantity)
        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

        content = {
            "basket_items": request.user.basket.all().order_by('product__category'),
            "media_url": settings.MEDIA_URL,
            }
        result = render_to_string("basketapp/includes/inc_basket_list.html", content)

        return JsonResponse({"result": result})
    