from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Custumer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __self__(self):
        return self.name  ## This is gonne be shown in the admin pannel


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(blank=True, null=True, default=False)  ##If it's digital, we do not ship it
    image = models.ImageField(blank=True, null=True, )

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    custumer = models.ForeignKey(Custumer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(blank=True, null=True, default=False)
    transactional_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()  # I have access to that cause of the OneOnOne
        for i in orderItems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name + "|" + self.order.transactional_id

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    custumer = models.ForeignKey(Custumer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    adress = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adress
