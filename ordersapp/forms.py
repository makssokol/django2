from ordersapp.models import Order, OrderItem
from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'is_active', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='price', min_length=1, 
                            max_length=18, required=False)
    
    class Meta:
        model = OrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    