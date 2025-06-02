from django.urls import path
from . import views
from .views import ContactMessageView

urlpatterns = [
    path('cakes/',views.cakes, name= 'cake'),
    path('latest/',views.latest_cakes, name='latest'),
    path('bestselling/',views.bestselling_cakes, name='bestselling'),
    path('cake_detail/<slug:slug>/',views.cake_detail, name= 'cake_detail'),
    path('add_cake/',views.add_cake, name= 'add_cake'),
    path('cake_in_cart',views.cake_in_cart,name='cake_in_cart'),
    path('get_cart_figures',views.get_cart_figures,name='cart_figures'),
    path('get_cart',views.get_cart,name='get_cart'),
    path('update_quantity/',views.update_quantity,name='update'),
    path('delete_cartitem/',views.delete_cartitem, name= 'delete'),
    path('contact/',ContactMessageView.as_view(),name='contact-message'),
    path('get_username',views.get_username,name='get_username'),
    path('get_user_info',views.get_user_info,name='user_info'),
    path('register/',views.register_user, name='register'),
    path('initiate_paypal_payment/', views.initiate_paypal_payment, name='initiate_paypal_payment'),
    path('paypal_payment_callback/', views.paypal_payment_callback, name='paypal_payment_callback'),
]
