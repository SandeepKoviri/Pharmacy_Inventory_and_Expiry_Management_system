from django.contrib import admin
from .models import Manufacturer, Medicine, Purchase, Sale


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "email")
    search_fields = ("name", "email", "contact")


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "generic_name", "manufacturer", "batch_number", "price", "stock", "expiry_date")
    list_filter = ("manufacturer", "expiry_date")
    search_fields = ("name", "generic_name", "batch_number")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "medicine", "supplier", "quantity", "purchase_price", "purchase_date", "created_by")
    list_filter = ("purchase_date",)
    search_fields = ("medicine__name", "supplier", "batch_number")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "medicine", "customer_name", "quantity", "selling_price", "sale_date", "created_by")
    list_filter = ("sale_date",)
    search_fields = ("medicine__name", "customer_name", "batch_number")
