from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import (
    SellerSerializer, MarketSerializer, SellerCreateSerializer, ProductSerializer, ProductDetailSerializer, ProductUpdateSerializer
)
from market_app.models import Seller, Market, Product

# ✅ ALLE MÄRKTE LISTEN ODER EINEN HINZUFÜGEN
@api_view(['GET', 'POST'])
def market_list(request):
    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data)

    if request.method == 'POST': 
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ EINZELNEN MARKT ABRUFEN, UPDATEN ODER LÖSCHEN
@api_view(['GET', 'PUT', 'DELETE'])
def market_detail(request, pk):
    market = get_object_or_404(Market, pk=pk)

    if request.method == 'GET':
        serializer = MarketSerializer(market)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = MarketSerializer(market, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        market.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ✅ ALLE VERKÄUFER LISTEN ODER EINEN HINZUFÜGEN
@api_view(['GET', 'POST'])
def seller_list(request):
    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SellerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ EINZELNEN VERKÄUFER ABRUFEN, UPDATEN ODER LÖSCHEN
@api_view(['GET', 'PUT', 'DELETE'])
def seller_detail(request, pk):
    seller = get_object_or_404(Seller, pk=pk)

    if request.method == 'GET':
        serializer = SellerSerializer(seller)
        return Response(serializer.data)

    if request.method == 'PUT':  # FIXED: War vorher POST, PUT ist korrekt!
        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ✅ ALLE PRODUKTE LISTEN ODER EINS HINZUFÜGEN
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == 'POST': 
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ EINZELNES PRODUKT ABRUFEN, UPDATEN ODER LÖSCHEN
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # FIXED: War vorher falsch definiert

    if request.method == 'GET':
        serializer = ProductDetailSerializer(product)  # FIXED: Nutze den Detail-Serializer für bessere Darstellung
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProductUpdateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product.delete()  # FIXED: War vorher nicht korrekt definiert
        return Response(status=status.HTTP_204_NO_CONTENT)
