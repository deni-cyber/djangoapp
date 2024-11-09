from django.contrib import admin
from .models import Category, Product, Review, ProductImage



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra image fields to display

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    
    def delete_model(self, request, obj):
        # Custom delete for Product in case you need more control
        obj.images.all().delete()  # This will call delete on each ProductImage
        obj.delete()


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Review)
