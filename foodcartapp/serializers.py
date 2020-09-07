from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ('address', 'firstname', 'lastname', 'phonenumber', 'products')

    def validate_products(self, value):
        if not value:
            raise ValidationError('Product list cannot be empty')

        return value
