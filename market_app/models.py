from django.db import models

# Verkäufer (Seller) Model
class Seller(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    markets = models.ManyToManyField("Market", related_name="market_sellers")  # Eindeutiger related_name

    def __str__(self):
        return self.name

# Markt (Market) Model
class Market(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sellers = models.ManyToManyField(Seller, related_name="seller_markets")  # Eindeutiger related_name

    def __str__(self):
        return self.name

# Produkt (Product) Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="market_products")  # Tippfehler korrigiert (market statt marktet)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="seller_products")  # Eindeutiger related_name

    def __str__(self):
        return f"{self.name} - {self.price} €"
