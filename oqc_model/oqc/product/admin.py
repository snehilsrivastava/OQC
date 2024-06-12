from django.contrib import admin
from .models import *

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('no', 'Date','ModelName')
#     ordering = ('no',)

class Product_detail_Admin(admin.ModelAdmin):
    list_display = ('no', 'ProductType','ModelName','SerailNo')
    ordering = ('no',)



admin.site.register(AC)
admin.site.register(Washing_Machine)
admin.site.register(Phone)
admin.site.register(TV)
admin.site.register(Product_Detail,Product_detail_Admin)

