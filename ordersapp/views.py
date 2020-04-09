from django.shortcuts import render
from ordersapp.models import Order, OrderItem
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from ordersapp.forms import OrderForm, OrderItemForm
from django.urls import reverse_lazy
from django.forms.models import inlineformset_factory
from basketapp.models import Basket
from django.db import transaction


class OrderList(ListView):
    model = Order
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

class OrderItemsCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('ordersapp:index')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)
        formset = None
        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        elif self.request.method == 'GET':
            basket_items = self.request.user.basket.all()
            if basket_items.count():
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                # basket_items.delete()
            else:
                formset = OrderFormSet()
                
        data['orderitems'] = formset
        return data        
    
    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user 
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            self.request.user.basket.all().delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)
        
        
class OrderItemsUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('ordersapp:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            data['orderitems'] = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        elif self.request.method == 'GET':
            data['orderitems'] = OrderFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)
    
class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:index')
    
    
class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'order/view'
        return context
    