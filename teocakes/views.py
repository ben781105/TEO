from .models import Cake, Cart, CartItem,ContactMessage,Transaction
from .serializers import CakeSerializer,DetailedCakeSerializer,CartItemSerializer,NumberCartSerializer, CartSerializer,ContactMessageSerializer,UserSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings
import paypalrestsdk
from django.views.decorators.csrf import csrf_exempt
import uuid
BASE_URL = settings.REACT_BASE_URL or 'http://localhost:5173'

paypalrestsdk.configure({
    'mode':settings.PAYPAL_MODE,
    'client_id':settings.PAYPAL_CLIENT_ID,
    'client_secret':settings.PAYPAL_CLIENT_SECRET
})
#BASE_URL = 'http://localhost:5173'
@api_view(['GET'])
def cakes(request):
    cakes = Cake.objects.all()
    serializer = CakeSerializer(cakes, many=True)
        
    return Response(serializer.data)

@api_view(['GET'])
def latest_cakes(request):
    cakes = Cake.objects.filter(is_latest = True)
    serializer = CakeSerializer(cakes, many=True)
        
    return Response(serializer.data)

@api_view(['GET'])
def bestselling_cakes(request):
    cakes = Cake.objects.filter(is_bestselling = True)
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

@csrf_exempt
@api_view(['POST'])
def initiate_paypal_payment(request):
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    tx_ref = str(uuid.uuid4())
    user = request.user
    cart_id = request.data.get('cart_id')

    if not cart_id:
        return Response({"error": "Cart ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    from decimal import Decimal

    amount = sum(Decimal(cake.cake.price) * Decimal(cake.quantity) for cake in cart.cakes.all())
    tax = amount * Decimal('0.18')
    total = amount + tax

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": f"{BASE_URL}/status?paymentStatus=success&tx_ref={tx_ref}",
            "cancel_url": f"{BASE_URL}/status?paymentStatus=cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Cart-item",
                    "sku": "cart",
                    "price": f"{total:.2f}",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": f"{total:.2f}",
                "currency": "USD"
            },
            "description": f"Payment for cart items for user"
        }]
    })

    transaction, created = Transaction.objects.get_or_create(
        tx_ref=tx_ref,
        cart=cart,
        user=user,
        amount=total,
        status='pending',
    )

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                return Response({'approvalUrl': str(link.href)}, status=status.HTTP_201_CREATED)

    return Response({'error': payment.error}, status=status.HTTP_400_BAD_REQUEST)

    # Add a default return statement
    return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(['POST'])
def paypal_payment_callback(request):
    # Extracting the query parameters from the URL
    payment_id = request.query_params.get('paymentId')
    payer_id = request.query_params.get('PayerID')
    tx_ref = request.query_params.get('tx_ref')

    try:
        transaction = Transaction.objects.get(tx_ref=tx_ref)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the transaction has already been completed
    if transaction.status == 'completed':
        return Response({'error': 'Payment has already been done for this cart.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check and execute the payment with PayPal SDK
    if payment_id and payer_id and tx_ref:
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({'payer_id': payer_id}):
            transaction.status = 'completed'
            transaction.save()
            cart = transaction.cart  
            cart.paid = True
            cart.user = request.user
            cart.save()
            return Response({'message': 'Your payment was processed successfully 🎉'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Payment execution failed'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)