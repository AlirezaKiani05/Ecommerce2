from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id', 'title', 'is_enable', 'created_time']
    list_filter = ['is_enable']
    search_fields = ['title']
    filter_horizontal = ['categories']
    
@admin.register(Category)
class CategoyAdmin(admin.ModelAdmin):
    list_display = ['parent', 'title', 'is_enable']
    list_filter = ['is_enable', 'parent']
    search_fields = ['title']    
    
    
  
