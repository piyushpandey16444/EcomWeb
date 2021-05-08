from django.urls import path
from .views import home_view, product_detail_view

urlpatterns = [
    path('', home_view, name='home'),
    path('product/', product_detail_view, name='product-detail'),
]
