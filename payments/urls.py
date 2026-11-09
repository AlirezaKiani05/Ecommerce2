from django.urls import path
from .views import GatewayView, PaymentView, PaymentVerifyView

app_name = 'payments'

urlpatterns = [
    path('gateways/', GatewayView.as_view(), name='gateways'),
    path('create/', PaymentView.as_view(), name='create'),
    path('verify/', PaymentVerifyView.as_view(), name='verify'),
]
