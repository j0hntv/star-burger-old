from rest_framework.serializers import ModelSerializer

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'quantity')


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('address', 'firstname', 'lastname', 'phonenumber')
