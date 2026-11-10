from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product,CommentModel,ReplyCommentModel


class ReplyCommentInline(admin.TabularInline):
    model = ReplyCommentModel
    extra = 0  
    fields = ['user', 'text', 'is_approved']
    readonly_fields = ['user', 'text'] 
    
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
    
@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'is_approved', 'created_time']
    list_editable = ['is_approved']  
    list_filter = ['is_approved', 'created_time']
    search_fields = ['text', 'user__username', 'product__title']
    inlines = [ReplyCommentInline] 
    
@admin.register(ReplyCommentModel)
class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comment', 'is_approved', 'created_time']
    list_editable = ['is_approved']
    list_filter = ['is_approved', 'created_time']
    search_fields = ['text', 'user__username']
    
  
