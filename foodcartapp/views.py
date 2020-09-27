from django.db import transaction
from django.templatetags.static import static
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderItem, Banner
from .serializers import OrderSerializer


def banners_list_api(request):
    banners = Banner.objects.all()
    return JsonResponse(
        [{'title': banner.title, 'src': banner.image.url, 'text': banner.text} for banner in banners],
        safe=False,
        json_dumps_params={'ensure_ascii': False, 'indent': 4,}
    )


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'ingridients': product.ingridients,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
@transaction.atomic
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    order = Order.objects.create(
        address=serializer.validated_data['address'],
        firstname=serializer.validated_data['firstname'],
        lastname=serializer.validated_data['lastname'],
        phonenumber=serializer.validated_data['phonenumber'],
    )

    product_fields = serializer.validated_data['products']
    products = [OrderItem(order=order, price=fields['product'].price, **fields) for fields in product_fields]
    OrderItem.objects.bulk_create(products)

    return Response(serializer.data)
