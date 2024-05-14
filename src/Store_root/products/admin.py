from django.contrib import admin

from products.models import ProductCotegory, Product, Basket

# Register your models here.
#admin.site.register(Product)
admin.site.register(ProductCotegory)
admin.site.register(Basket)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quontity', 'categoty')
    fields = ('name', 'image', 'description', 'short_description', ('price', 'quontity'), 'categoty')
    readonly_fields = ['short_description']
    ordering = ['-name']
    search_fields = ['name', 'price']


class BasketAdminInLine(admin.TabularInline):
    model = Basket
    fields = ('product', 'quontity', 'created_timestamp')
    readonly_fields = ['created_timestamp', 'product']
    extra = 0
