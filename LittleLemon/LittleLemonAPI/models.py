from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField()
    
    def __str__(self)-> str:
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True, default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    
    def __str__(self)-> str:
        return self.title

# Each User can only have one Cart at a time.
# When a User tries to add a menuitem to the Cart, it first needs to be checked if this
# menuitem is already present in the Cart's table. If so, it needs to update the quantity
# for this menuitem. If the menuitem is not in the table, then it is necessary to add one
# record for this menuitem.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'menuitem')


# When the User places the order, then first it is created one new record in the Order
# table with the order's basic information. Then, all of the data in the Cart table is
# "moved" to the OrderItem table. Lastly, the records from the Cart table for that
# particular User are deleted, so that when the same User wants to start over adding
# MenuItems to his/her Cart, the Cart is empty and there isn't any issues.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(db_index=True, default=False)      # To indicate if the Order is considered as:
                                                                    # "pending"   (status = False), or
                                                                    # "delivered" (status = True).
    date = models.DateField(db_index=True, auto_now=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)     # Price of all the MenuItems in this Order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')