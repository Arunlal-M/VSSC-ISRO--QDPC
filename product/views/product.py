# product/views/product.py

from django.shortcuts import render

def product_home(request):
    return render(request, 'product/index.html')  
