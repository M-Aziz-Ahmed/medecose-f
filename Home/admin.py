from django.contrib import admin
from .models import Product, Category, ProductVariant, CartItem, ProductImage,Blog, Contact,ProductType,Order,OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(CartItem)
admin.site.register(ProductType)
admin.site.register(Order)
admin.site.register(OrderItem)

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

    # Filter images to only show those for the specific product
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(product=self.parent_object)

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_object = obj  # Store the current product object
        return super().get_formset(request, obj, **kwargs)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Blog)

