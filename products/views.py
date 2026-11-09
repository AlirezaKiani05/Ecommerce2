import uuid
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .serializers import ProductSerializer, CategorySerializer
from payments.models import Gateway, Payment
from .models import Category, Product

# baray inke to postman be moshkel nakhorim vali moghe deploy bardar in kelas CsrfExemptSessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


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


class ProductPayView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, pk):

        product = get_object_or_404(Product, pk=pk, is_enable=True)

        gateway_id = request.data.get('gateway')
        if not gateway_id:
            return Response(
                {'detail': 'Please provide the gateway ID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        gateway = get_object_or_404(Gateway, pk=gateway_id, is_enable=True)

        user_phone = None
        if hasattr(request.user, 'profile') and request.user.profile.phone_number:
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

        return Response({
            'detail': 'Factors are ready to pay',
            'token': payment.token,
            'price': payment.price,
            'product_title': product.title,
            'gateway_title': gateway.title,
            'mock_callback_url': 'http://127.0.0.1:8000/api/payments/verify/'
        }, status=status.HTTP_201_CREATED)
