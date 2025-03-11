from rest_framework import serializers
from market_app.models import Seller, Market, Product

# 🛍️ Seller Serializer (CRUD)
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

# 🏪 Market Serializer (CRUD)
class MarketSerializer(serializers.ModelSerializer):
    sellers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Seller.objects.all(), read_only=False
    )

    class Meta:
        model = Market
        fields = '__all__'

    def create(self, validated_data):
        sellers = validated_data.pop('sellers', [])
        market = Market.objects.create(**validated_data)
        market.sellers.set(sellers)
        return market

    def update(self, instance, validated_data):
        if 'sellers' in validated_data:
            instance.sellers.set(validated_data.pop('sellers'))
        return super().update(instance, validated_data)

# 🏪 Market Detail Serializer (Nur für GET)
class MarketDetailSerializer(serializers.ModelSerializer):
    sellers = SellerSerializer(many=True, read_only=True)

    class Meta:
        model = Market
        fields = '__all__'

# 🛍️ Seller Detail Serializer (Nur für GET)
class SellerDetailSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)  # Read-only gesetzt

    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'phone', 'address', 'markets']

# 🛍️ Seller Create Serializer (Nur für POST)
class SellerCreateSerializer(serializers.ModelSerializer):
    markets = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = Seller
        fields = ['id', 'name', 'email', 'phone', 'address', 'markets']

    def validate_markets(self, value):
        markets = Market.objects.filter(pk__in=value)
        if len(value) != len(markets):
            raise serializers.ValidationError("Ein oder mehrere Märkte existieren nicht.")
        return value

    def create(self, validated_data):
        market_ids = validated_data.pop('markets', [])
        seller = Seller.objects.create(**validated_data)
        seller.markets.set(Market.objects.filter(id__in=market_ids))
        return seller

# 🛍️ Seller Update Serializer (Nur für PUT/PATCH)
class SellerUpdateSerializer(serializers.ModelSerializer):
    markets = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = Seller
        fields = ['name', 'email', 'phone', 'address', 'markets']

    def validate_markets(self, value):
        markets = Market.objects.filter(pk__in=value)
        if len(value) != len(markets):
            raise serializers.ValidationError("Ein oder mehrere Märkte existieren nicht.")
        return value

    def update(self, instance, validated_data):
        if "markets" in validated_data:
            instance.markets.set(Market.objects.filter(id__in=validated_data.pop("markets", [])))
        return super().update(instance, validated_data)

# 🏪 Product Serializer (CRUD)
class ProductSerializer(serializers.ModelSerializer):
    market = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

# 🏪 Product Detail Serializer (Nur für GET)
class ProductDetailSerializer(serializers.ModelSerializer):
    market = MarketSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

# 🏪 Product Create Serializer (Nur für POST)
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        market_id = data.get('market', None)
        seller_id = data.get('seller', None)

        if market_id and not Market.objects.filter(id=market_id).exists():
            raise serializers.ValidationError({"market": "Market-ID existiert nicht."})

        if seller_id and not Seller.objects.filter(id=seller_id).exists():
            raise serializers.ValidationError({"seller": "Seller-ID existiert nicht."})

        return data

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

# 🏪 Product Update Serializer (Nur für PUT/PATCH)
class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'market', 'seller']

    def validate(self, data):
        market_id = data.get('market', None)
        seller_id = data.get('seller', None)

        if market_id and not Market.objects.filter(id=market_id).exists():
            raise serializers.ValidationError({"market": "Market-ID existiert nicht."})

        if seller_id and not Seller.objects.filter(id=seller_id).exists():
            raise serializers.ValidationError({"seller": "Seller-ID existiert nicht."})

        return data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
