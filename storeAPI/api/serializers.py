from rest_framework import serializers
from .models import Category, Product

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category", "created_at", "updated_at"]