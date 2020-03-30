from django.db import models
from django.conf import settings
from mainapp.models import ArtObject

# Create your models here.

class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="basket", on_delete=models.CASCADE)
    product = models.ForeignKey(ArtObject, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="quantity", default=0)
    add_datetime = models.DateTimeField(verbose_name="add time", auto_now_add=True)

    @property
    def product_cost(self):
        "return total cost of all art objects of this type"
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        "return total quantity for user"
        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        "return total cost for user"
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost
