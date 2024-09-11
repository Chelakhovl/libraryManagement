from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'created_at')
    list_display_links = ('book', 'user')
    list_filter = ('book', 'user')
    search_fields = ('book', 'user')
    

