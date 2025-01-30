from django.contrib import admin
from . models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )}
    list_display = ['name', 'slug']

admin.site.register(Product_Model)
admin.site.register(Brand_Model)
admin.site.register(Category_Model, CategoryAdmin)
admin.site.register(Review_Model)

