from rest_framework.views import APIView

from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.db import transaction

from django.core.paginator import Paginator, EmptyPage
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from decimal import Decimal

from .models import (Category, MenuItem, Cart, Order, OrderItem)
from .serializers import (UserSerializer, CategorySerializerDetailed,
                          MenuItemSerializerDetailed, CartSerializer,
                          OrderSerializerSimple, OrderSerializerDetailed)

# ##################################
# Global Variables
# ##################################
DEFAULT_PERPAGE = 5
MAX_PERPAGE = 20



# ##################################
# 2. User group management endpoints
# ##################################

# endpoint: /api/groups/manager/users
# Accepts GET and POST methods
# Only for authenticated users in the Managers group
# GET:  Returns all managers
# POST: Assigns the user in the payload to the manager group and returns 201-Created
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def manager(request):
    if not request.user.groups.filter(name='Manager').exists():
        # If the user performing this action doesn't belong to the Manager group
        return Response({"message": "You don't belong to the Manager group."}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        # Returns all managers list
        managersList = User.objects.filter(groups = Group.objects.get(name="Manager"))
        serialized_managersList = UserSerializer(managersList, many=True)
        return Response(serialized_managersList.data, status=status.HTTP_200_OK)
        
    elif request.method == 'POST':
        # Assigns the username in the payload to the manager group and returns 201-Created
        
        try:
            username = request.data['username']
        except:
            # If the username in the payload wasn't passed...
            return Response({"message": "It must be passed a 'username' variable in the payload."}, status=status.HTTP_400_BAD_REQUEST)
            
        if username:
            # If the username in the payload was passed...
            
            # If this next instruction returns a 404 error code,
            # this means that the passed username doesn't exist
            # in the User model.
            user = get_object_or_404(User, username=username)
            
            # Adds the user to the Manager's group
            managersGroup = Group.objects.get(name="Manager")
            managersGroup.user_set.add(user)
            
            # And removes the user from the Delivery crew's group, in case it belonged to it,
            # because a user cannot belong to two groups at the same time.
            deliveryCrewGroup = Group.objects.get(name="Delivery crew")
            deliveryCrewGroup.user_set.remove(user)
            
            message = 'The user: ' + username + ' was set as a Manager.'
            return Response({"message": message}, status=status.HTTP_201_CREATED)



# endpoint: /api/groups/manager/users/{userId}
# Accepts DELETE method
# Only for authenticated users in the Managers group
# DELETE: Removes this particular user from the manager group and returns 200 – Success if everything is okay.
#         If the user is not found, returns 404 – Not found
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def manager_delete(request, userId):
    if not request.user.groups.filter(name='Manager').exists():
        # If the user performing this action doesn't belong to the Manager group
        return Response({"message": "You don't belong to the Manager group."}, status=status.HTTP_403_FORBIDDEN)
    
    user = get_object_or_404(User, id=userId)
    username = user.get_username()
    if user.groups.filter(name='Manager').exists():
        # If user belongs to the Manager group, then remove user from group
        managersGroup = Group.objects.get(name="Manager")
        managersGroup.user_set.remove(user)
        message = 'The user: ' + username + ' was just removed as a Manager.'
        return Response({"message": message}, status=status.HTTP_200_OK)
    else:
        # If user doesn't belong to the Maganer group
        message = "The user: " + username + " doesn't belong to the Manager group."
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)



# endpoint: /api/groups/delivery-crew/users
# Accepts GET and POST methods
# Only for authenticated users in the Managers group
# GET:  Returns all Delivery crews
# POST: Assigns the user in the payload to the Delivery crew group and returns 201-Created
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def delivery(request):
    if not request.user.groups.filter(name='Manager').exists():
        # If the user performing this action doesn't belong to the Manager group
        return Response({"message": "You don't belong to the Manager group."}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        # Returns all Delivery crew list
        deliveryCrewList = User.objects.filter(groups = Group.objects.get(name="Delivery crew"))
        serialized_deliveryCrewList = UserSerializer(deliveryCrewList, many=True)
        return Response(serialized_deliveryCrewList.data, status=status.HTTP_200_OK)
        
    elif request.method == 'POST':
        # Assigns the username in the payload to the Delivery crew group and returns 201-Created
        
        try:
            username = request.data['username']
        except:
            # If the username in the payload wasn't passed...
            return Response({"message": "It must be passed a 'username' variable in the payload."}, status=status.HTTP_400_BAD_REQUEST)
            
        if username:
            # If the username in the payload was passed...
            
            # If this next instruction returns a 404 error code,
            # this means that the passed username doesn't exist
            # in the User model.
            user = get_object_or_404(User, username=username)
            
            # Adds the user to the Delivery crew's group
            deliveryCrewGroup = Group.objects.get(name="Delivery crew")
            deliveryCrewGroup.user_set.add(user)
            
            # And removes the user from the Manager's group, in case it belonged to it,
            # because a user cannot belong to two groups at the same time.
            managersGroup = Group.objects.get(name="Manager")
            managersGroup.user_set.remove(user)
            
            message = 'The user: ' + username + ' was set as a Delivery crew.'
            return Response({"message": message}, status=status.HTTP_201_CREATED)



# endpoint: /api/groups/delivery-crew/users/{userId}
# Accepts DELETE method
# Only for authenticated users in the Managers group
# DELETE: Removes this particular user from the Delivery crew group and returns 200 – Success if everything is okay.
#         If the user is not found, returns 404 – Not found
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def delivery_delete(request, userId):
    if not request.user.groups.filter(name='Manager').exists():
        # If the user performing this action doesn't belong to the Manager group
        return Response({"message": "You don't belong to the Manager group."}, status=status.HTTP_403_FORBIDDEN)
    
    user = get_object_or_404(User, id=userId)
    username = user.get_username()
    if user.groups.filter(name='Delivery crew').exists():
        # If user belongs to the Delivery crew group, then remove user from group
        deliveryCrewGroup = Group.objects.get(name="Delivery crew")
        deliveryCrewGroup.user_set.remove(user)
        message = 'The user: ' + username + ' was just removed as a Delivery crew.'
        return Response({"message": message}, status=status.HTTP_200_OK)
    else:
        # If user doesn't belong to the Delivery crew group
        message = "The user: " + username + " doesn't belong to the Delivery crew group."
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)




# ##################################
# 3. Category endpoints
# ##################################

# endpoint: /api/category
# Accepts GET and POST methods
# GET (for any user, authenticated or unauthenticated):
# Lists all Categories. Returns a 200 – Ok HTTP status code.
# POST (Only for authenticated Managers): Creates a new Category and returns 201 - Created.
class CategoryView(APIView):
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':    # Another way of writing this line is: # if self.request.method in ['POST', 'DELETE']:
            # Every HTTP request method that is defined in this class, excepting the GET method, will require authentication.
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def get(self, request):
        categories = Category.objects.all()
        serialized_categories = CategorySerializerDetailed(categories, many=True)
        return Response(serialized_categories.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            # If User is in the Manager group
            # 
            # Here in request.data, we need to receive:
            # category_title and slug.
            # 
            # Creates a new Category and returns 201 - Created
            serialized_category = CategorySerializerDetailed(data=request.data)
            serialized_category.is_valid(raise_exception=True)
            serialized_category.save()
            return Response(serialized_category.data, status=status.HTTP_201_CREATED)
        else:
            # If the requesting User is not in the Manager group
            # Denies access and returns 403 – Unauthorized HTTP status code
            return Response({"message": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)



# endpoint: /api/category/{categoryId}
# Accepts GET, PUT, PATCH and DELETE methods
# GET (for any user, authenticated or unauthenticated):
# Lists single Category. Returns 200 – Ok HTTP status code
# PUT and PATCH (Only for authenticated Managers): Updates a single Category and returns 200 - OK status code.
# DELETE (Only for authenticated Managers): Deletes a single Category and returns 200 - OK status code.
class CategorySingleView(APIView):
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            # Every HTTP request method that is defined in this class, excepting the GET method, will require authentication.
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def get(self, request, categoryId):
        category = get_object_or_404(Category, pk=categoryId)
        serialized_category = CategorySerializerDetailed(category)
        return Response(serialized_category.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, categoryId):
        if request.user.groups.filter(name='Manager').exists():
            # If User is in the Manager group
            category = get_object_or_404(Category, pk=categoryId)
            serialized_category = CategorySerializerDetailed(category, data=request.data, partial=True)
            serialized_category.is_valid(raise_exception=True)
            serialized_category.save()
            return Response(serialized_category.data, status=status.HTTP_200_OK)
        else:
            # If the requesting User is not in the Manager group (but is Delivery crew or Customer)
            # Denies access and returns 403 – Unauthorized HTTP status code
            return Response({"message": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
    
    
    def patch(self, request, categoryId):
        # Call the put method with the same arguments to avoid duplication
        return self.put(request, categoryId)
    
    
    def delete(self, request, categoryId):
        if request.user.groups.filter(name='Manager').exists():
            # If User is in the Manager group
            category = get_object_or_404(Category, pk=categoryId)
            category.delete()
            return Response({"message": "Deleted."}, status=status.HTTP_200_OK)
        else:
            # If the requesting User is not in the Manager group (but is Delivery crew or Customer)
            # Denies access and returns 403 – Unauthorized HTTP status code
            return Response({"message": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)




# ##################################
# 4. Menu-items endpoints
# ##################################

# endpoint: /api/menu-items
# Accepts GET and POST methods
# GET (for any user, authenticated or unauthenticated):
# Lists all MenuItems. Returns a 200 – Ok HTTP status code.
# POST (Only for authenticated Managers): Creates a new MenuItem and returns 201 - Created.
class MenuItemView(APIView):
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            # Every HTTP request method that is defined in this class, excepting the GET method, will require authentication.
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def get(self, request):
        # Lists all menu items. Return a 200 – Ok HTTP status code
        # 
        # It doesn't matter the User's group:
        # Manager, Delivery crew or any of the previous 2 groups (Customer).
        
        menuItems = MenuItem.objects.select_related('category').all()
        
        # Filtering
        category_name = request.query_params.get('category')    # Filter by category name
        from_price = request.query_params.get('from_price')     # Filter from a specific price
        to_price = request.query_params.get('to_price')         # Filter up to a specific price
        price = request.query_params.get('price')               # Filter by a specific price
        
        # Searching
        search = request.query_params.get('search')
        
        # Ordering or sorting
        ordering = request.query_params.get('ordering')
        
        # Pagination
        perpage = int(request.query_params.get('perpage', default=DEFAULT_PERPAGE))
        page = int(request.query_params.get('page', default=1))
        
        if perpage > MAX_PERPAGE:
            return Response({"message": "perpage cannot be greater than {}.".format(MAX_PERPAGE)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Applying filters
        if category_name:
            menuItems = menuItems.filter(category__title__icontains=category_name)  # __icontains: Case-insensitive containment test.
        if from_price:
            menuItems = menuItems.filter(price__gte=from_price)
        if to_price:
            menuItems = menuItems.filter(price__lte=to_price)
        if price:
            menuItems = menuItems.filter(price=price)
        
        # Applying search
        if search:
            menuItems = menuItems.filter(title__icontains=search)
        
        # Applying sorting
        if ordering:
            menuItems = menuItems.order_by(ordering)
        
        # Pagination
        paginator = Paginator(menuItems, per_page=perpage)
        try:
            menuItems = paginator.page(number=page)
        except EmptyPage:
            menuItems = []
        
        serialized_menuItems = MenuItemSerializerDetailed(menuItems, many=True)
        return Response(serialized_menuItems.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            # If User is in the Manager group
            
            input_format = request.query_params.get('input-format')
            if input_format == 'json':
                # If input-format is equal to json:
                menu_items_data = request.data  # This will be the list of menu items

                if not isinstance(menu_items_data, list):
                    return Response({"message": "Data must be in list format."}, status=status.HTTP_400_BAD_REQUEST)

                created_items = []  # To hold the serialized items created

                for item_data in menu_items_data:
                    try:
                        category_id = item_data['category_id']
                    except KeyError:
                        return Response({"message": "Each item must have a 'category_id' variable."}, status=status.HTTP_400_BAD_REQUEST)

                    category = get_object_or_404(Category, pk=category_id)

                    # Prepare the MenuItem data
                    menuitem_data = {
                        "title": item_data['title'],
                        "price": Decimal(item_data['price']),  # Convert to Decimal
                        "featured": item_data.get('featured', False),
                        "category": category  # Passing the Category instance
                    }

                    # Create the MenuItem instance directly
                    menuitem = MenuItem.objects.create(**menuitem_data)
                    created_items.append(menuitem)

                # Serialize all created MenuItems
                serialized_menuItems = MenuItemSerializerDetailed(created_items, many=True)
                return Response(serialized_menuItems.data, status=status.HTTP_201_CREATED)
            
            
            # If input-format is NOT equal to json:
            
            # Here in request.data, we need to receive:
            # title, price, featured and category_id.
            # 
            # Creates a new menu item and returns 201 - Created
            
            try:
                category_id = request.data['category_id']
            except KeyError:
                return Response({"message": "It must be passed a 'category_id' variable in the payload."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Convert category_id to a Category instance
            category = get_object_or_404(Category, pk=category_id)
            
            # Prepare the MenuItem data
            menuitem_data = {
                "title": request.data['title'],
                "price": Decimal(request.data['price']),  # Converting string price to Decimal
                "featured": request.data.get('featured', False),
                "category": category  # Passing the Category instance
            }
            
            # Create the MenuItem instance directly
            menuitem = MenuItem.objects.create(**menuitem_data)
            
            # Serialize the created MenuItem
            serialized_menuItem = MenuItemSerializerDetailed(menuitem)
            
            return Response(serialized_menuItem.data, status=status.HTTP_201_CREATED)
            
        else:
            # If the requesting User is not in the Manager group (but is Delivery crew or Customer)
            # Denies access and returns 403 – Unauthorized HTTP status code
            return Response({"message": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)



# endpoint: /api/menu-items/{menuitemId}
# Accepts GET, PUT, PATCH and DELETE methods
# GET (for any user, authenticated or unauthenticated):
# Lists single MenuItem. Returns 200 – Ok HTTP status code
# PUT and PATCH (Only for authenticated Managers): Updates a single MenuItem and returns 200 - OK status code.
# DELETE (Only for authenticated Managers): Deletes a single MenuItem and returns 200 - OK status code.
class MenuItemSingleView(APIView):
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            # Every HTTP request method that is defined in this class, excepting the GET method, will require authentication.
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def get(self, request, menuitemId):
        menuItem = get_object_or_404(MenuItem, pk=menuitemId)
        serialized_menuItem = MenuItemSerializerDetailed(menuItem)
        return Response(serialized_menuItem.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, menuitemId):
        if request.user.groups.filter(name='Manager').exists():
            # If requesting User is in the Manager group
            menuItem = get_object_or_404(MenuItem, pk=menuitemId)

            # Extract the data from the request
            title = request.data.get('title', menuItem.title)                   # Use existing value if not provided
            price = request.data.get('price', menuItem.price)                   # Same for price
            featured = request.data.get('featured', menuItem.featured)          # Same for featured
            category_id = request.data.get('category_id', menuItem.category)

            # Handle the category_id update or keep the current category if not provided
            category_id = request.data.get('category_id', None)
            if category_id:
                # If category_id was provided...
                category = get_object_or_404(Category, pk=category_id)  # gets the new category
            else:
                # If category_id was NOT provided...
                category = menuItem.category  # keeps the existing category

            # Update the fields
            menuItem.title = title
            menuItem.price = Decimal(price)
            menuItem.featured = featured
            menuItem.category = category    # Updates the category (whether the old if NOT provided, or the new if provided)

            # Save the updated MenuItem
            menuItem.save()

            # Serialize and return the updated MenuItem
            serialized_menuItem = MenuItemSerializerDetailed(menuItem)
            return Response(serialized_menuItem.data, status=status.HTTP_200_OK)
        else:
            # If the requesting User is not in the Manager group (but is Delivery crew or Customer)
            # Denies access and returns 403 – Unauthorized HTTP status code
            return Response({"message": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
    
    
    def patch(self, request, menuitemId):
        # Call the put method with the same arguments to avoid duplication
        return self.put(request, menuitemId)
    
    
    def delete(self, request, menuitemId):
        if request.user.groups.filter(name='Manager').exists():
            # If requesting User is in the Manager group
            menuItem = get_object_or_404(MenuItem, pk=menuitemId)
            menuItem.delete()
            return Response({"message": "Deleted."}, status=status.HTTP_200_OK)
        else:
            # If the requesting User is not in the Manager group (but is Delivery crew or Customer)
            # Denies access and returns 403 – Unauthorized HTTP status code
            return Response({"message": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)




# endpoint: /api/menu-items/item-of-the-day
# Accepts GET, PUT and PATCH methods
# GET (for any user, authenticated or unauthenticated):
# Lists all MenuItem(s) of the day (MenuItem.featured = True). Returns 200 – Ok HTTP status code
# 
# PUT and PATCH (Only for authenticated Managers): Updates MenuItem.featured = False for every MenuItem that was
# previously set as True, and assigns the current MenuItem.featured = True for the single MenuItem that was passed
# as an argument with the variable menuitemId. Then returns 200 - OK status code.
class MenuItemOfTheDayView(APIView):
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            # Every HTTP request method that is defined in this class, excepting the GET method, will require authentication.
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def get(self, request):
        menuItems = get_list_or_404(MenuItem, featured=True)
        serialized_menuItems = MenuItemSerializerDetailed(menuItems, many=True)
        return Response(serialized_menuItems.data, status=status.HTTP_200_OK)
    
    
    def put(self, request):
        if request.user.groups.filter(name='Manager').exists():
            # If User is in the Manager group
            menuitemId = request.data.get('menuitemId', None)
            
            if menuitemId:
                if menuitemId.isnumeric() and int(menuitemId) > 0:
                    menuitemId = int(menuitemId)
                    menuItemOfTheDay = get_object_or_404(MenuItem, pk=menuitemId)
                    
                    menuItemsFeatured = MenuItem.objects.all()
                    menuItemsFeatured = menuItemsFeatured.filter(featured=True)
                    
                    for menuItemFeatured in menuItemsFeatured:
                        menuItemFeatured.featured = False
                        menuItemFeatured.save()
                    
                    menuItemOfTheDay.featured = True
                    menuItemOfTheDay.save()
                    
                    serialized_menuItemOfTheDay = MenuItemSerializerDetailed(menuItemOfTheDay)
                    return Response(serialized_menuItemOfTheDay.data, status=status.HTTP_200_OK)
                    
                else:
                    return Response({"message": "The variable menuitemId should be a possitive and integer number."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "The variable menuitemId should be provided."}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            # If the requesting User is not in the Manager group (but is Delivery crew or Customer)
            # Denies access and returns 403 – Unauthorized HTTP status code
            return Response({"message": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
    
    
    def patch(self, request):
        # Call the put method with the same arguments to avoid duplication
        return self.put(request)




# ##################################
# 5. Cart management endpoint
# ##################################

# endpoint: /api/cart/menu-items
# Accepts GET, POST and DELETE methods for Customers
# GET: Returns current items in the cart for the current user token
# POST: Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items
# DELETE: Deletes all menu items created by the current user token
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def cart(request):
    if request.method == 'GET':
        try:
            # Get all cart items for the user
            cart_items = Cart.objects.select_related('menuitem').filter(user=request.user)
            if not cart_items.exists():
                return Response({"message": "The cart is empty."}, status=status.HTTP_200_OK)

            # Serialize the cart items grouped by user
            serialized_cart = CartSerializer(request.user)  # Pass the user to the serializer
            return Response(serialized_cart.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        try:
            user_id = request.user.id
            menuitem_id = request.data.get('menuitem')
            quantity = int(request.data.get('quantity'))

            # Get the user and menuitem
            user = get_object_or_404(User, id=user_id)
            menuitem = get_object_or_404(MenuItem, id=menuitem_id)

            # Check if the item is already in the cart
            cart_item, created = Cart.objects.get_or_create(
                user=user,
                menuitem=menuitem,
                defaults={'quantity': quantity, 'unit_price': Decimal(menuitem.price), 'price': Decimal(quantity * Decimal(menuitem.price))}
            )

            if not created:
                # Update the quantity and price if the item already exists
                cart_item.quantity += quantity
                cart_item.price = Decimal(cart_item.quantity) * Decimal(cart_item.unit_price)
                cart_item.save()

            # Get all cart items for the user and serialize
            serialized_cart = CartSerializer(request.user)  # Pass the user to the serializer
            return Response(serialized_cart.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:  # DELETE method
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items.exists():
                cart_items.delete()
                return Response({"message": "Cart deleted."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Cart is already empty."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




# ##################################
# 6. Order management endpoint
# ##################################

# endpoint: /api/orders
# Accepts GET and POST methods from anyone.
# GET: Returns current items in the cart for the current user token
# POST: Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def orders(request):
    if request.method == 'GET':
        
        if request.user.groups.filter(name='Manager').exists():
            # If the requesting User sending the GET request belongs to the Managers group
            # Returns all orders with order items by all users
            all_orders = Order.objects.all()
            if not all_orders.exists():
                return Response({"message": "No orders have been made in the system yet."}, status=status.HTTP_200_OK)

            # Filtering
            user_id = request.query_params.get('user_id')       # Filter by user ID
            order_status = request.query_params.get('status')   # Filter by order status
            from_date = request.query_params.get('from_date')   # Filter from a specific date. Ex: ?from_date=20241017
            to_date = request.query_params.get('to_date')       # Filter up to a specific date. Ex: ?to_date=20241016

            # Searching
            search = request.query_params.get('search')         # Search by username

            # Sorting
            ordering = request.query_params.get('ordering')     # Sort results

            # Pagination
            perpage = int(request.query_params.get('perpage', default=DEFAULT_PERPAGE))
            page = int(request.query_params.get('page', default=1))

            if perpage > MAX_PERPAGE:
                return Response({"message": "perpage cannot be greater than {}.".format(MAX_PERPAGE)}, status=status.HTTP_400_BAD_REQUEST)

            # Applying filters
            if user_id:
                all_orders = all_orders.filter(user__id=user_id)
            if order_status:
                if order_status.lower() == 'pending':
                    all_orders = all_orders.filter(status=False)
                elif order_status.lower() == 'delivered':
                    all_orders = all_orders.filter(status=True)
                else:
                    return Response({"message": "status should be either 'pending' or 'delivered'."}, status=status.HTTP_400_BAD_REQUEST)
            if from_date:
                all_orders = all_orders.filter(date__gte=from_date)
            if to_date:
                all_orders = all_orders.filter(date__lte=to_date)
            
            # Applying search
            if search:
                all_orders = all_orders.filter(user__username__icontains=search)
            
            # Applying sorting
            if ordering:
                all_orders = all_orders.order_by(ordering)
            
            # Pagination
            paginator = Paginator(all_orders, per_page=perpage)
            try:
                all_orders = paginator.page(number=page)
            except EmptyPage:
                all_orders = []
            
            serialized_orders = OrderSerializerDetailed(all_orders, many=True)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)
        elif request.user.groups.filter(name='Delivery crew').exists():
            # If the User sending the GET request belongs to the Delivery crews group
            # Returns all orders with order items assigned to the delivery crew
            delivery_crew_orders = Order.objects.filter(delivery_crew=request.user)
            if not delivery_crew_orders.exists():
                return Response({"message": "{} hasn't received any orders for delivery yet.".format(request.user)}, status=status.HTTP_200_OK)
            
            
            # Filtering
            order_status = request.query_params.get('status')   # Filter by order status
            from_date = request.query_params.get('from_date')   # Filter from a specific date. Ex: ?from_date=20241017
            to_date = request.query_params.get('to_date')       # Filter up to a specific date. Ex: ?to_date=20241016

            # Searching
            search = request.query_params.get('search')         # Search by username

            # Sorting
            ordering = request.query_params.get('ordering')     # Sort results

            # Pagination
            perpage = int(request.query_params.get('perpage', default=DEFAULT_PERPAGE))
            page = int(request.query_params.get('page', default=1))

            if perpage > MAX_PERPAGE:
                return Response({"message": "perpage cannot be greater than {}.".format(MAX_PERPAGE)}, status=status.HTTP_400_BAD_REQUEST)

            # Applying filters
            if order_status:
                if order_status.lower() == 'pending':
                    delivery_crew_orders = delivery_crew_orders.filter(status=False)
                elif order_status.lower() == 'delivered':
                    delivery_crew_orders = delivery_crew_orders.filter(status=True)
                else:
                    return Response({"message": "status should be either 'pending' or 'delivered'."}, status=status.HTTP_400_BAD_REQUEST)
            if from_date:
                delivery_crew_orders = delivery_crew_orders.filter(date__gte=from_date)
            if to_date:
                delivery_crew_orders = delivery_crew_orders.filter(date__lte=to_date)
            
            # Applying search
            if search:
                delivery_crew_orders = delivery_crew_orders.filter(user__username__icontains=search)
            
            # Applying sorting
            if ordering:
                delivery_crew_orders = delivery_crew_orders.order_by(ordering)
            
            # Pagination
            paginator = Paginator(delivery_crew_orders, per_page=perpage)
            try:
                delivery_crew_orders = paginator.page(number=page)
            except EmptyPage:
                delivery_crew_orders = []
            
            
            serialized_orders = OrderSerializerDetailed(delivery_crew_orders, many=True)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)
        else:
            # If the User sending the GET request belongs to the Customers group
            # Returns all orders with order items created by this user
            customer_orders = Order.objects.filter(user=request.user)
            if not customer_orders.exists():
                return Response({"message": "{} hasn't placed any orders yet.".format(request.user)}, status=status.HTTP_200_OK)
            
            serialized_orders = OrderSerializerSimple(customer_orders, many=True)
            return Response(serialized_orders.data, status=status.HTTP_200_OK)
    else:   # POST method
        # If the User has a Cart with menuItems added to it...
        cart_items = Cart.objects.select_related('menuitem').filter(user=request.user)
        if not cart_items.exists():
            return Response({"message": "For placing an order, first there must be items added to the cart."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the total price for the order
        total_price = sum([item.price for item in cart_items])

        # Create a new order record
        try:
            with transaction.atomic():
                # The transaction.atomic() ensures that either all actions succeed or none, avoiding data inconsistencies
                
                new_order = Order.objects.create(
                    user=request.user,
                    delivery_crew=None,   # No delivery crew initially assigned
                    total=total_price
                )

                # Populate the OrderItem model with Cart data
                order_items = []
                for cart_item in cart_items:
                    order_items.append(OrderItem(
                        order=new_order,
                        menuitem=cart_item.menuitem,
                        quantity=cart_item.quantity,
                        unit_price=cart_item.unit_price,
                        price=cart_item.price
                    ))

                # Bulk create all OrderItems at once for efficiency
                OrderItem.objects.bulk_create(order_items)

                # Clear the user's cart after the order is placed
                cart_items.delete()

                # Return the newly created order data
                serialized_order = OrderSerializerSimple(new_order)
                return Response(serialized_order.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# endpoint: /api/orders/{orderId}
# Accepts GET, PUT, PATCH and DELETE methods
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def order_single(request, orderId):
    if request.user.groups.filter(name='Manager').exists():
        if request.method == 'DELETE':
            order = get_object_or_404(Order, pk=orderId)
            order.delete()
            return Response({"message": "Order deleted."}, status=status.HTTP_200_OK)
        elif request.method == 'PUT' or request.method == 'PATCH':
            
            order = get_object_or_404(Order, pk=orderId)
            delivery_crew = request.data.get('delivery_crew', default=None)     # Defaults = Null
            order_status = request.data.get('status', default=None)             # Defaults = Null
            
            message = []
            
            # If delivery_crew is not passed as an argument, leave the order.delivery_crew as it was before
            if delivery_crew is not None:
                # Here delivery_crew was passed as an argument
                if delivery_crew == 'Null':
                    order.delivery_crew = None
                elif delivery_crew.isnumeric():
                    delivery_user = get_object_or_404(User, pk=delivery_crew)
                    if not delivery_user.groups.filter(name='Delivery crew').exists():
                        # If the delivery_crew doesn't belong to the Delivery crew group
                        return Response({"message": "delivery_crew user doesn't belong to the Delivery crew group."}, status=status.HTTP_400_BAD_REQUEST)
                    
                    order.delivery_crew = delivery_user
                else:
                    message.append("delivery_crew should be either an integer number or 'Null'.")
            
            # If status is not passed as an argument, leave the order.status as it was before
            if order_status is not None:
                # Here status was passed as an argument
                if order_status == 'delivered' or order_status == 'Delivered':
                    # If status == 'delivered', set order.status = True
                    order.status = True
                elif order_status == 'pending' or order_status == 'Pending':
                    # And if status == 'pending', set order.status = False
                    order.status = False
                else:
                    message.append("status should be either 'pending' or 'delivered'.")
            
            if len(message) > 0:
                return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
            
            order.save()
            
            serialized_order = OrderSerializerDetailed(order)
            return Response(serialized_order.data, status=status.HTTP_200_OK)
            
        else:
            return Response({"message": "Method Not Allowed for Manager users."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif request.user.groups.filter(name='Delivery crew').exists():
        if request.method == 'PATCH':
            order = get_object_or_404(Order, pk=orderId)
            
            if order.delivery_crew == request.user:
                # If the user sending the PATCH request is the same that is assigned as the Delivery crew for this Order
                order_status = request.data.get('status', default=None)         # Defaults = Null
                
                # If status is not passed as an argument, leave the order.status as it was before
                if order_status is not None:
                    # Here status was passed as an argument
                    if order_status == 'delivered' or order_status == 'Delivered':
                        # If status == 'delivered', set order.status = True
                        order.status = True
                    elif order_status == 'pending' or order_status == 'Pending':
                        # And if status == 'pending', set order.status = False
                        order.status = False
                    else:
                        return Response({"message": "status should be either 'pending' or 'delivered'."}, status=status.HTTP_400_BAD_REQUEST)
                    
                    order.save()
                
                serialized_order = OrderSerializerDetailed(order)
                return Response(serialized_order.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
            
        else:
            return Response({"message": "Method Not Allowed for Delivery crew users."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        # If the User sending the request belongs to the Customers group
        if request.method == 'GET':
            order = get_object_or_404(Order, pk=orderId)
            if order.user == request.user:
                # If the customer user sending the GET request was the same customer user that made the order...
                serialized_order = OrderSerializerSimple(order)
                return Response(serialized_order.data, status=status.HTTP_200_OK)
            else:
                # If the customer user sending the GET request was NOT the same customer user that made the order...
                return Response({"message": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Method Not Allowed for Customer users."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




# ##################################
# 7. Additional endpoints
# ##################################

# endpoint: /api/users/all
# Accepts GET method
# Only for users in the Managers group
# GET:  Returns a list of all users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def all_users(request):
    if not request.user.groups.filter(name='Manager').exists():
        # If the user performing this action doesn't belong to the Manager group
        return Response({"message": "You don't belong to the Manager group."}, status=status.HTTP_403_FORBIDDEN)
    
    # Returns all managers list
    usersList = User.objects.all()
    serialized_usersList = UserSerializer(usersList, many=True)
    return Response(serialized_usersList.data, status=status.HTTP_200_OK)