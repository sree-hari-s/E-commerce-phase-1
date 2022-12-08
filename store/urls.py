from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),#homepage
    path('cart/',views.cart,name='cart'),#cart
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('products/',views.products,name='products'),#products page
    path('product-detail/',views.product_detail,name='product-detail'),#specific products
    path('wishlist',views.wishlist,name='wishlist'),#wishlist
    path('login/',views.loginPage,name='login'),
    path('register',views.registerPage,name='register'),
    path('logout/',views.logoutUser,name='logout'),   
    path('profile/',views.profile,name='profile'),
]