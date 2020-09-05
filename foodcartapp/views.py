import json

from django.templatetags.static import static
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


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
def register_order(request):
    data=request.data

    products = data.get('products')
    address = data.get('address')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    phonenumber = data.get('phonenumber')

    if not all((products, isinstance(products, list))):
        return Response({'error': 'There is no order item or it\'s not a list'}, status=status.HTTP_400_BAD_REQUEST)

    if not all((address, isinstance(address, str))):
        return Response({'error': 'The key \'address\' is not specified or not a str'}, status=status.HTTP_400_BAD_REQUEST)

    if not all((firstname, isinstance(firstname, str))):
        return Response({'error': 'The key \'firstname\' is not specified or not a str'}, status=status.HTTP_400_BAD_REQUEST)

    if not all((lastname, isinstance(lastname, str))):
        return Response({'error': 'The key \'lastname\' is not specified or not a str'}, status=status.HTTP_400_BAD_REQUEST)

    if not all((phonenumber, isinstance(phonenumber, str))):
        return Response({'error': 'The key \'phonenumber\' is not specified or not a str'}, status=status.HTTP_400_BAD_REQUEST)

    available_products = Product.objects.all()
    product_ids = set([product.id for product in available_products])
    received_ids = set([product['product'] for product in products])

    if not received_ids.issubset(product_ids):
        return Response({'error': f'Product id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        address=address,
        firstname=firstname,
        lastname=lastname,
        phonenumber=phonenumber,
    )

    products = data['products']
    for product in products:
        current_product = Product.objects.get(id=product['product'])
        OrderItem.objects.create(
            order=order,
            product=current_product,
            quantity=product['quantity'],
        )

    return Response({})
