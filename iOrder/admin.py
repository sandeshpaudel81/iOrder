from django.contrib import admin
from iOrder.models import *

# Register your models here.
admin.site.register(Table)
admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Transaction)
