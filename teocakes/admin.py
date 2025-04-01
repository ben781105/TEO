from django.contrib import admin
from .models import Cake, Cart,CartItem,ContactMessage,Transaction
# Register your models here.
admin.site.register(Cake)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ContactMessage)
admin.site.register(Transaction)
