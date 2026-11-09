from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):

    title = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(
        _('avatar'), blank=True, upload_to='categories/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created_time'), auto_now_add=True)
    updated_time = models.DateField(_('updated_time'), auto_now=True)
    parent = models.ForeignKey('self', verbose_name=_(
        'parent'), blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    price = models.PositiveIntegerField(_('price'), default=0)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='products/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    categories = models.ManyToManyField(
        'Category', verbose_name=_('categoties'), blank=True)
    created_time = models.DateTimeField(_('created_time'), auto_now_add=True)
    updated_time = models.DateField(_('updated_time'), auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "products"
        verbose_name = 'product'
        verbose_name_plural = 'products'
        
        
