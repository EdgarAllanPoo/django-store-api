from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreate.as_view(), name='category-view-create'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroy.as_view(), name='category-retrieve-update-destroy'),
    path('products/', views.ProductListCreate.as_view(), name='product-view-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view(), name='product-retrieve-update-destroy'),
]