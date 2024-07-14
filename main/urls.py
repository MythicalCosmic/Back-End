from django.urls import path
from .views import *

urlpatterns = [
    path('api-auth/login/', login_view, name='api-auth-login'),
    path('api-auth/logout/', logout_view, name='api-auth-logout'),
    path('api/products/all', allProducts, name='api-products-all'),
    path('api/products/create', createProduct, name='api-products-create'),
    path('api/products/delete/<int:pk>', deleteProduct, name='api-products-delete'),
    path('api/products/update/<int:pk>', updateProduct, name='api-products-update'),
    path('api/category/all', allCategory, name='api-category-all'),
    path('api/category/create', createCategory, name='api-category-create'),
    path('api/category/delete/<int:pk>', deleteCategory, name='api-category-delete'),
    path('api/category/update/<int:pk>', updateCategory, name='api-category-update'),
]