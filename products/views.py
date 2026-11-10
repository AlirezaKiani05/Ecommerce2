import uuid
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from .serializers import (
    ProductListSerializer, CategorySerializer, CommentSerializer, ReplyCommentSerializer, ProductDetailSerializer
)
from payments.models import Gateway, Payment
from .models import Category, Product, CommentModel, ReplyCommentModel

# baray inke to postman be moshkel nakhorim vali moghe deploy bardar in kelas CsrfExemptSessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.all()

        serializer = ProductListSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        serializer = ProductDetailSerializer(
            product,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


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


class ProductPayView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, pk):
        product = get_object_or_404(
            Product,
            pk=pk,
            is_enable=True
        )

        gateway_id = request.data.get('gateway')

        if not gateway_id:
            return Response(
                {'detail': 'Please provide the gateway ID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        gateway = get_object_or_404(
            Gateway,
            pk=gateway_id,
            is_enable=True
        )
        user_phone = None
        if (
            hasattr(request.user, 'profile')
            and request.user.profile.phone_number
        ):
            user_phone = request.user.profile.phone_number

        payment_token = uuid.uuid4().hex

        payment = Payment.objects.create(
            user=request.user,
            gateway=gateway,
            product=product,
            price=product.price,
            phone_number=user_phone,
            token=payment_token,
            status=Payment.STATUS_PENDING
        )

        return Response(
            {
                'detail': 'Factor is ready to pay.',
                'token': payment_token,
                'price': payment.price,
                'product_title': product.title,
                'gateway_title': gateway.title,
                'mock_callback_url':
                    'http://127.0.0.1:8000/api/payments/verify/',
            },
            status=status.HTTP_201_CREATED
        )


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(product=product, user=request.user,
                            is_approved=True)
            return Response({"detail":
                            "Your comment has been registered and will be displayed after approval."},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateReplyCommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, comment_pk):
        parent_comment = get_object_or_404(CommentModel, pk=comment_pk)
        serializer = ReplyCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(comment=parent_comment,
                            user=request.user, is_approved=True)
            return Response({"detail": "Your comment has been registered and will be displayed after approval"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
