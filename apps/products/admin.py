from django.contrib import admin
from .models import Product, ProductImage


# TODO: limit max image per product to 5!
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5  # How many empty image fields to display

    def save_related(self, request, form, change):
        # Ensure the parent object is saved first
        super().save_related(request, form, change)
        for instance in formset.instance:
            # Your custom logic here if needed
            instance.save()  # Ensure each image is saved


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "image_count", "description")
    list_filter = ("price",)  # Add filter options
    search_fields = ("title", "description")  # Enable search on these fields
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
