from django.urls import path

from .views import (CategoryListView, ProductListView,  ProductDetailView
                   ,CategoryDetailView,ProductPayView,CreateCommentView,CreateReplyCommentView
                )
                  

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
    path('products/<int:pk>/pay/', ProductPayView.as_view(), name='product-pay'),
    
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(),
         name='category-detail'),
    
    path('products/<int:product_pk>/comments/', CreateCommentView.as_view(), name='add-comment'),
    path('comments/<int:comment_pk>/replies/', CreateReplyCommentView.as_view(), name='add-reply'),
]
