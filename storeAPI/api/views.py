from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Category, Product
from .serializers import CategorySerializers, ProductSerializers
from django.core.cache import cache
from rest_framework.response import Response
from django.utils.http import urlencode

# Create your views here.
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get(self, request, *args, **kwargs):
        cached_data = cache.get("store:categories")
        if cached_data:
            return Response(cached_data)

        response = super().get(request, *args, **kwargs)
        cache.set("store:categories", response.data, timeout=60 * 5)  
        return response

    def perform_create(self, serializer):
        serializer.save()

        cache.clear() # cleared all due to category is a FK

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save()

        cache.clear() # cleared all due to category is a FK

    def perform_destroy(self, instance):
        instance.delete()

        cache.clear() # cleared all due to category is a FK

class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = {
        'category__name': ['exact'],  
        'price': ['gte', 'lte'],     
    }

    ordering_fields = ['price', 'name']  

    cache_keys = []  

    def get(self, request, *args, **kwargs):
        query_params = urlencode(request.query_params, doseq=True)
        cache_key = f"store:products:{query_params}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().get(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        self.cache_keys.append(cache_key) 
        return response

    def invalidate_cache(self):
        for cache_key in self.cache_keys:
            cache.delete(cache_key)  

    def perform_create(self, serializer):
        serializer.save()

        self.invalidate_cache()

class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'

    cache_keys = ProductListCreate.cache_keys

    def perform_update(self, serializer):
        serializer.save()

        self.invalidate_cache()

    def perform_destroy(self, instance):
        instance.delete()

        self.invalidate_cache()

    def invalidate_cache(self):
        for cache_key in self.cache_keys:
            cache.delete(cache_key)  