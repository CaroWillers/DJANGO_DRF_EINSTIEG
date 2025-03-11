from django.urls import path
from market_app.api.views import seller_list, seller_detail, market_list, market_detail, product_list, product_detail

urlpatterns = [
    # Seller Endpunkte
    path('sellers/', seller_list, name='seller-list'),
    path('seller/<int:pk>/', seller_detail, name='seller-detail'),

    # Market Endpunkte
    path('markets/', market_list, name='market-list'),
    path('market/<int:pk>/', market_detail, name='market-detail'),

    # Product Endpunkte
    path('products/', product_list, name='product-list'),
    path('product/<int:pk>/', product_detail, name='product-detail'),
]
