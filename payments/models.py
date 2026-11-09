from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.validators import phone_number_validator


class Gateway(models.Model):
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), max_length=150, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='gateways/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('update'), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'gateways'
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PENDING = 1
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCELED = 30
    STATUS_REFUNDED = 31

    STATUS_CHOICES = (
        (STATUS_VOID, _('void')),
        (STATUS_PENDING, _('pending')),
        (STATUS_PAID, _('paid')),
        (STATUS_ERROR, _('error')),
        (STATUS_CANCELED, _('canceled')),
        (STATUS_REFUNDED, _('refunded')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='payments',
        on_delete=models.CASCADE
    )
    gateway = models.ForeignKey(
        Gateway,
        verbose_name=_('gateway'),
        related_name='payments',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'products.Product',
        verbose_name=_('product'),
        related_name='payments',
        on_delete=models.CASCADE
    )
    price = models.PositiveBigIntegerField(_('price'), default=0)
    status = models.PositiveSmallIntegerField(
        _('status'),
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True
    )
    device_uuid = models.CharField(_('device_uuid'), blank=True, max_length=40)

    phone_number = models.CharField(
        _('phone_number'),
        max_length=15,
        blank=True,
        null=True,
        validators=[phone_number_validator],
        db_index=True
    )
    consumed_code = models.PositiveIntegerField(
        _('consumed reference code'),
        null=True,
        blank=True,
        db_index=True
    )

    token = models.CharField(
        _('token'),
        max_length=64,
        unique=True,
        db_index=True
    )
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update'), auto_now=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.product.title} - Status: {self.get_status_display()}"

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
