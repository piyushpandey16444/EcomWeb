from django.shortcuts import render


def home_view(request):
    return render(request, 'shop/home.html')


def product_detail_view(request):
    return render(request, 'shop/product-detail.html')
