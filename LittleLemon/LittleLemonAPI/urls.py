from django.urls import path
from . import views
# from rest_framework.authtoken.views import obtain_auth_token
 
urlpatterns = [
    
    # 2. User group management endpoints
    path('groups/manager/users', views.manager),
    path('groups/manager/users/<int:userId>', views.manager_delete),
    path('groups/delivery-crew/users', views.delivery),
    path('groups/delivery-crew/users/<int:userId>', views.delivery_delete),
    
    # 3. Category endopoints
    path('category', views.CategoryView.as_view()),
    path('category/<int:categoryId>', views.CategorySingleView.as_view()),
    
    # 4. Menu-items endpoints
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:menuitemId>', views.MenuItemSingleView.as_view()),
    path('menu-items/item-of-the-day', views.MenuItemOfTheDayView.as_view()),
    
    # 5. Cart management endpoint
    path('cart/menu-items', views.cart),
    
    # 6. Order management endpoints
    path('orders', views.orders),
    path('orders/<int:orderId>', views.order_single),
    
    # 7. Additional endpoints
    path('users/all', views.all_users),
    
]
