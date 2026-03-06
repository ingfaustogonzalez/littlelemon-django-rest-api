from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import (Category, MenuItem, Cart, Order, OrderItem)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


# To be used in the menuitems endpoints
class CategorySerializerSimple(serializers.ModelSerializer):
    category_title = serializers.CharField(max_length=255, source='title')
    class Meta:
        model = Category
        fields = ['category_title']  # Only serialize the category's title


# To be used in the category endpoints
class CategorySerializerDetailed(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='id', default=None)
    category_title = serializers.CharField(max_length=255, source='title')
    # slug = serializers.SlugField()
    class Meta:
        model = Category
        fields = ['category_id', 'category_title', 'slug']      # Display all the details


class MenuItemSerializerSimple(serializers.ModelSerializer):
    category_id = CategorySerializerSimple()    # Use the CategorySerializerSimple to get just
                                                # the category name
    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'featured', 'category_id']  # Include category in the serialized output


class MenuItemSerializerDetailed(serializers.ModelSerializer):
    category = CategorySerializerSimple()     # Use the CategorySerializerDetailed to get all the
                                                # category's information
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']  # Include category in the serialized output


class CartItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.CharField(source='menuitem.title')  # Get the title of the MenuItem
    category = serializers.CharField(source='menuitem.category.title')  # Get the title of the Category
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['menuitem', 'category', 'unit_price', 'quantity', 'price']

    def get_price(self, cart):
        # Calculate the price for each cart item
        return round(cart.quantity * cart.unit_price, 2)


class CartSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()  # This variable will hold all cart items

    class Meta:
        model = Cart
        fields = ['cart']

    def get_cart(self, obj):
        # Since `obj` is now a `User` object, get their cart items directly
        cart_items = Cart.objects.filter(user=obj).select_related('menuitem')  # Filter by user
        return CartItemSerializer(cart_items, many=True).data  # Serialize the cart items


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.CharField(source='menuitem.title')  # Display menu item title
    class Meta:
        model = OrderItem
        fields = ['menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializerSimple(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    status = serializers.SerializerMethodField()    # Use SerializerMethodField to customize the output
    total = serializers.DecimalField(max_digits=6, decimal_places=2)
    order_items = OrderItemSerializer(many=True, source='orderitem_set')  # Include order items

    class Meta:
        model = Order
        fields = ['id', 'username', 'status', 'date', 'total', 'order_items']
    
    def get_status(self, obj):
        # Custom method to return "pending" or "delivered"
        return "delivered" if obj.status else "pending"


class OrderSerializerDetailed(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    delivery_crew = serializers.CharField()
    status = serializers.SerializerMethodField()    # Use SerializerMethodField to customize the output
    total = serializers.DecimalField(max_digits=6, decimal_places=2)
    order_items = OrderItemSerializer(many=True, source='orderitem_set')  # Include order items

    class Meta:
        model = Order
        fields = ['id', 'username', 'status', 'delivery_crew', 'date', 'total', 'order_items']
    
    def get_status(self, obj):
        # Custom method to return "pending" or "delivered"
        return "delivered" if obj.status else "pending"