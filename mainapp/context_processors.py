def basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.select_related('product__category').all()
    return {
        'basket': basket,
    }