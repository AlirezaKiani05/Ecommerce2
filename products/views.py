from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer ,CategorySerializer
from .models import Category, Product

class ProductListView(APIView):

    def get(self, request):
        print(request.user)
        print(request.auth)
        products = Product.objects.all()
        context = {'request': request}
        serializer = ProductSerializer(products, many=True, context=context)
        return Response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryDetailView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)
