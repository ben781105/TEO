from .models import Cake, Cart, CartItem,ContactMessage
from .serializers import CakeSerializer,DetailedCakeSerializer,CartItemSerializer,NumberCartSerializer, CartSerializer,ContactMessageSerializer,UserSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from decimal import Decimal
import uuid
from django.conf import settings
BASE_URL =settings.REACT_BASE_URL
#BASE_URL = 'http://localhost:5173'
@api_view(['GET'])
def cakes(request):
    cakes = Cake.objects.all()
    serializer = CakeSerializer(cakes, many=True)
        
    return Response(serializer.data)
@api_view(['GET'])
def cake_detail(request,slug):
    cake = Cake.objects.get(slug=slug)
    serializer = DetailedCakeSerializer(cake)
    return Response(serializer.data)


@api_view(['POST'])
def add_cake(request):
    try:
        cart_id = request.data.get('cart_id')
        cake_id = request.data.get('cake_id')

        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
        cake = Cake.objects.get(id=cake_id)

        cartitem, created = CartItem.objects.get_or_create(cart=cart, cake=cake)
        cartitem.quantity = 1
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response({"data":serializer.data, "message":"Cart created successfully", "status":201})
    except Exception as e:
        return Response({"error":str(e), "status":400})
    

@api_view(['GET'])    
def cake_in_cart(request):
    cart_id = request.query_params.get('cart_id')
    cake_id = request.query_params.get('cake_id')

    cart = Cart.objects.get(cart_id=cart_id)
    cake = Cake.objects.get(id=cake_id)

    cake_exits = CartItem.objects.filter(cart=cart,cake=cake).exists()
    return Response({'cake_in_cart': cake_exits})

@api_view(['GET'])
def get_cart_figures(request):
    cart_id =request.query_params.get('cart_id')
    cart = Cart.objects.get(cart_id=cart_id,paid=False)
    serializer = NumberCartSerializer(cart)
    return Response(serializer.data)

@api_view(['GET'])
def get_cart(request):
  cart_id = request.query_params.get('cart_id')
  cart = Cart.objects.get(cart_id=cart_id,paid=False)
  serializer = CartSerializer(cart)
  return Response(serializer.data)


@api_view(['PATCH'])
def update_quantity(request):
    try:
        cartitem_id = request.data.get('cartitem_id')
        quantity = request.data.get('quantity')
        quantity =int(quantity)
        cartitem =CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({"data":serializer.data,"message":"Cartitem updated successfully"})
    except Exception as e:
        return Response({"error": str(e)},status=400)
        
@api_view(['POST'])
def delete_cartitem(request):
    cartitem_id = request.data.get('cartitem_id')
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return Response({'message':'Item removed successfully'},status=status.HTTP_204_NO_CONTENT)

class ContactMessageView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Your message has been received successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    return Response({'username':user.username})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def register_user(request):
    user= get_user_model()
    data = request.data
    if user.objects.filter(username=data['username']).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    user = user.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )

    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


