import uuid
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from products.models import Product
from .models import Gateway, Payment
from .serializers import GatewaySerializer
from rest_framework.authentication import SessionAuthentication

# baray inke to postman be moshkel nakhorim vali moghe deploy bardar in kelas CsrfExemptSessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # CSRF check is disable
    
class GatewayView(APIView):
    

    def get(self, request):
        gateways = Gateway.objects.filter(is_enable=True)
        serializer = GatewaySerializer(gateways, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentView(APIView):

    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        gateway_id = request.data.get('gateway')
        product_id = request.data.get('product')

        if not gateway_id or not product_id:
            return Response(
                {'detail': 'Please fill the gateway and product fields.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, pk=product_id, is_enable=True)
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
            'mock_callback_url': 'http://127.0.0.1:8000/api/payments/verify/'
        }, status=status.HTTP_201_CREATED)


class PaymentVerifyView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        payment_token = request.data.get('token')
        action_status = request.data.get('status', 10)

        if not payment_token:
            return Response({'detail': 'sending token is required'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            payment = get_object_or_404(
                Payment.objects.select_for_update(),
                token=payment_token,
                user=request.user
            )

            if payment.status == Payment.STATUS_PAID:
                return Response({'detail': 'This paymant has already successful'}, status=status.HTTP_200_OK)

            if int(action_status) != 10:
                payment.status = Payment.STATUS_CANCELED
                payment.save(update_fields=['status', 'update_time'])
                return Response({'detail': 'Paymnet cancelled '}, status=status.HTTP_400_BAD_REQUEST)

            payment.status = Payment.STATUS_PAID
            payment.save(update_fields=['status', 'update_time'])

        return Response({
            'detail': 'Payment was successful',
            'product': payment.product.title,
            'price_paid': payment.price,
            'status': 'Paid'
        }, status=status.HTTP_200_OK)
