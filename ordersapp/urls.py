from django.urls import path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='index'),
    path('create/', ordersapp.OrderItemsCreate.as_view(), 
         name='order_create'),
    path('read/<int:pk>/', ordersapp.OrderRead.as_view(), 
         name='order_read'),
    path('update/<int:pk>/', ordersapp.OrderItemsUpdate.as_view(), 
         name='order_update'), 
    path('delete/<int:pk>/', ordersapp.OrderDelete.as_view(), 
         name='order_delete'), 
]
