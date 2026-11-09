from django.contrib import admin
from .models import Payment, Gateway


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_enable', 'created_time']
    list_filter = ['is_enable']
    search_fields = ['title']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = [
        'id', 'user', 'gateway', 'product',
        'price', 'status', 'phone_number', 'token', 'created_time'
    ]

    list_filter = ['status', 'gateway', 'product', 'created_time']
    search_fields = ['user__username', 'user__email', 'phone_number', 'token']

# Fields that the admin should not modify manually, to avoid corrupting financial data.
    readonly_fields = ['token', 'created_time',
                       'update_time', 'price', 'consumed_code']
