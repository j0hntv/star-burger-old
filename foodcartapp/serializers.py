from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, write_only=True)
    class Meta:
        model = Order
        fields = ('id', 'address', 'firstname', 'lastname', 'phonenumber', 'products')

    def validate_products(self, value):
        if not value:
            raise serializers.ValidationError('Product list cannot be empty')

        return value
