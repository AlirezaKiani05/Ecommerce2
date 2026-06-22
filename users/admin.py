from django.contrib import admin
from .models import Profile, Country

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display=['user','phone_number','country']
#     search_fields=['user']
    
# @admin.register(Country)
# class CountryAdmin(admin.ModelAdmin):
#     list_display=['name','is_active']
#     search_fields=['name']    
    

from django.contrib import admin
from .models import Profile, Country

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_email', 'phone_number', 'country']
    search_fields = ['user__username', 'user__email', 'phone_number']
    list_filter = ['country', 'user__is_active']
    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active'] 
