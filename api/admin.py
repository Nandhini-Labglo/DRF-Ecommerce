from django.contrib import admin
from .models import (
    Brand, 
    Product,
    Cart,
    Order,
    Wishlistitems,
    Payment
)

# Register your models here.


class Brandadmin(admin.ModelAdmin):
    list_display = ['id','brand_name','brand_logo']
admin.site.register(Brand, Brandadmin)

class productadmin(admin.ModelAdmin):
    list_display = ['id','title','image','price','in_stock']
admin.site.register(Product, productadmin)

class cartadmin(admin.ModelAdmin):
    list_display = ['id','product','user','quantity','is_active','price']
admin.site.register(Cart, cartadmin)

class orderadmin(admin.ModelAdmin):
    list_display = ['id','user','status',]
admin.site.register(Order, orderadmin)

class wishadmin(admin.ModelAdmin):
    list_display = ['id','user']
admin.site.register(Wishlistitems, wishadmin)

class paymentadmin(admin.ModelAdmin):
    list_display = ['id','order','transaction_id','payment_status',]
admin.site.register(Payment, paymentadmin)