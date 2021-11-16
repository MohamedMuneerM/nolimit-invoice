from django.contrib import admin
from . import models
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fk_name = "invoice"

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]


admin.site.register(models.User)
admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Organization)
admin.site.register(models.Item)
admin.site.register(models.OrderItem)
admin.site.register(models.Tax)


