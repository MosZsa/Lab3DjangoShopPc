from django.contrib import admin
from .models import Category, Product, Order, OrderItem
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('product', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at') 
    search_fields = ('name',) 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at') 
    list_filter = ('category',)  
    search_fields = ('name', 'description') 


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'status')  
    list_filter = ('status', 'created_at')  
    search_fields = ('id', 'user__username')  
    list_editable = ('status',)  


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price') 
    list_filter = ('order',)  
