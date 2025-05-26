from django.contrib import admin
from .models import Service, RequestedService

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'field', 'price_per_hour', 'date_created', 'company')
    search_fields = ('name', 'field', 'company__username')
    list_filter = ('field', 'date_created')