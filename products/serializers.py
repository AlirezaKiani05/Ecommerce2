
from rest_framework import serializers

from .models import  Product, Category
from payments.models import Gateway
from payments.serializers import GatewaySerializer


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'description', 'avatar', 'url']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
    checkout_url = serializers.SerializerMethodField()
    available_gateways = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['id','title', 'description','price','categories', 'url','checkout_url','available_gateways']
        
    def get_checkout_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/api/products/{obj.pk}/pay/")
        return f"/api/products/{obj.pk}/pay/"

    def get_available_gateways(self, obj):
        gateways = Gateway.objects.filter(is_enable=True)
        return GatewaySerializer(gateways, many=True).data
