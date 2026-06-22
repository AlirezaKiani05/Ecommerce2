
from rest_framework import serializers

from .models import  Product, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'description', 'avatar', 'url']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)


    class Meta:
        model = Product
        fields = ['id','title', 'description', 'categories', 'url']

