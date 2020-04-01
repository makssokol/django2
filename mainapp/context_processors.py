def basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.all()
    return {
        'basket': basket,
    }