from django.contrib import admin
# from .models import related models
from .models import CarMake
from .models import CarModel


# Register your models here.
# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = [
        'year',
        'car_make',
        'type'
    ]


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'description'
    ]
    inlines = [CarModelInline]


# Register models here

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
