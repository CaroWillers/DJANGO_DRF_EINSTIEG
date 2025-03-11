# 📌 Django Serializers für Seller & Market

Diese Datei enthält verschiedene Serializers für die Verarbeitung von `Seller` und `Market` Objekten in Django REST Framework.

## 1️⃣ `MarketSerializer` (CRUD für Märkte)
- Verwaltet **Market-Objekte**.
- Speichert und aktualisiert **Sellers für einen Market** (Many-to-Many).
- **Verwendet `sellers` als `PrimaryKeyRelatedField`.**

## 2️⃣ `SellerSerializer` (CRUD für Verkäufer)
- Verwaltet **Seller-Objekte**.
- Speichert und aktualisiert **Markets für einen Seller** (Many-to-Many).
- **Verwendet `markets` als `PrimaryKeyRelatedField`.**

## 3️⃣ `SellerDetailSerializer` (Nur für GET-Anfragen)
- **Nested Serializer**: Gibt `markets` als vollständige Objekte zurück.
- **Read-Only**, weil es keine `create` oder `update` Methode hat.

## 4️⃣ `SellerCreateSerializer` (Nur für POST)
- Spezieller Serializer für die Erstellung eines `Seller`.
- Erwartet eine **Liste von Market-IDs** (`ListField`).
- **Prüft in `validate_markets()`, ob alle Markets existieren.**
- Erstellt `Seller` und verknüpft die validierten Märkte.
