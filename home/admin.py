from django.contrib import admin
from home.models import Farm, Income, Expenditure


# Register your models here.
admin.site.register(Farm)
admin.site.register(Income)
admin.site.register(Expenditure)