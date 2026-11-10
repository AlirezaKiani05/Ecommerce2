from rest_framework import serializers
from .models import Product, Category, CommentModel, ReplyCommentModel
from payments.models import Gateway
from payments.serializers import GatewaySerializer


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'description', 'avatar', 'url']


class ReplyCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ReplyCommentModel
        fields = ['id', 'user', 'text', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    replies = serializers.SerializerMethodField()

    class Meta:
        model = CommentModel
        fields = ['id', 'user', 'text', 'created_time', 'replies']

    def get_replies(self, obj):
        approved_replies = obj.replies.filter(is_approved=True)

        return ReplyCommentSerializer(
            approved_replies,
            many=True,
            context=self.context
        ).data



class ProductListSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'categories',
            'url',
        ]


class ProductDetailSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    checkout_url = serializers.SerializerMethodField()
    available_gateways = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'categories',
            'url',
            'checkout_url',
            'available_gateways',
            'comments',
        ]

    def get_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True)

        return CommentSerializer(
            approved_comments,
            many=True,
            context=self.context
        ).data

    def get_checkout_url(self, obj):
        request = self.context.get('request')
        relative_url = f'/api/products/{obj.pk}/pay/'

        if request:
            return request.build_absolute_uri(relative_url)

        return relative_url

    def get_available_gateways(self, obj):
        gateways = Gateway.objects.filter(is_enable=True)

        return GatewaySerializer(
            gateways,
            many=True,
            context=self.context
        ).data

