from django.urls import path
from .views import (home_view, product_detail_view, signup_view, login_view,
                    verification_view, logout_view, cart_view, add_to_cart)

urlpatterns = [
    path('', home_view, name='home'),
    path('product/', product_detail_view, name='product-detail'),

    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('activate/<uid64>/<token>', verification_view, name='activate'),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/', add_to_cart, name="add-to-cart")
]
