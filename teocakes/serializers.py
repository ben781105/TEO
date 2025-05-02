from rest_framework import serializers
from .models import Cake, Cart,CartItem,ContactMessage
from django.contrib.auth import get_user_model
class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields =['id','name','slug','image','description','category','price']

class DetailedCakeSerializer(serializers.ModelSerializer):
    similar_cakes = serializers.SerializerMethodField()
    class Meta:
        model = Cake
        fields =['id','name','slug','image','description','category','price','similar_cakes']

    def get_similar_cakes(self,cake):
        cakes = Cake.objects.filter(category=cake.category).exclude(id=cake.id)
        serializer = CakeSerializer(cakes, many=True)
        return serializer.data
    

class CartItemSerializer(serializers.ModelSerializer):
    cake = CakeSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields =['id','cake','quantity','total']

    def get_total(self,cartitem):
        price = cartitem.cake.price * cartitem.quantity
        return price

    
class CartSerializer(serializers.ModelSerializer):
    cakes = CartItemSerializer(read_only=True, many=True)
    total = serializers.SerializerMethodField()
    num_cakes = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields =['id','cart_id','created_at','modified_at','total','cakes','num_cakes']
    
    def get_total(self,cart):
        cakes = cart.cakes.all()
        total = [cake.cake.price * cake.quantity for cake in cakes]
        return (total)
    
    def get_num_cakes(self, cart):
        cakes = cart.cakes.all()
        total =sum([cake.quantity for cake in cakes])
        return total


class NumberCartSerializer(serializers.ModelSerializer):
    num_of_cakes = serializers.SerializerMethodField()
    class Meta:
        model= Cart
        fields = ['id','cart_id','num_of_cakes']
        
    def get_num_of_cakes(self,cart):
            num_of_cakes = sum([cake.quantity for cake in cart.cakes.all()])
            return num_of_cakes
    

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class NewCartItemSerializer(serializers.ModelSerializer):
    cake = CakeSerializer(read_only=True)
    order_id =serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields =['id','cake','quantity','order_id','order_date']

    def get_order_id(self,cartitem):
        order_id = cartitem.cart.cart_id
        return order_id
    def get_order_date(self, cartitem):
        return cartitem.cart.modified_at.date().isoformat()

class UserSerializer(serializers.ModelSerializer):
    ordered_cakes = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields =['id','City','username','first_name','last_name','Phone','Address','email','ordered_cakes']

    def get_ordered_cakes(self,user):
        cartitems = CartItem.objects.filter(cart__user= user,cart__paid = True)
        serializer = NewCartItemSerializer(cartitems,many=True)
        return serializer.data