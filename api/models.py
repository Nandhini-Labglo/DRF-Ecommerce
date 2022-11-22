from django.db import models
from django.contrib.auth.models import User

# Create your models here.

FAILED = 0
SUCCESS = 1
PENDING = 2

ORDER_STATUS_CHOICES = (
    (SUCCESS, 'Success'),
    (FAILED, 'Failed'),
    (PENDING, 'Pending'),
)  

PAYMENT_STATUS_CHOICES = (
    (SUCCESS, 'Success'),
    (FAILED, 'Failed'),
    (PENDING, 'Pending'),
)  

class TimeStampBaseModel(models.Model):
    created_on =  models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 

class Brand(TimeStampBaseModel):
    brand_name = models.CharField(max_length=30)
    brand_logo = models.ImageField(upload_to='images/brands')
     
    def __str__(self):
        return '{}'.format(self.brand_name)


class Product(TimeStampBaseModel):
    title = models.CharField(max_length=30)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products')
    price = models.FloatField()
    description = models.TextField(max_length=120, blank=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.title)

class Cart(TimeStampBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    is_active = models.BooleanField()

    def __str__(self):
        return '{}'.format(self.product)

    
    def get_total(self):
        total = self.price * self.quantity
        return total

    def get_tax(self):
        grand_total = (18/100) * (self.get_total())
        return grand_total



class Order(TimeStampBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Cart)
    status = models.IntegerField(default=2, choices=ORDER_STATUS_CHOICES)
    total_order_price = models.FloatField()
    def __str__(self):
        return '{}'.format(self.id)

    def get_total_price(self):
        total = 0
        for order_item in self.product.all():
            total += order_item.get_total()
        return total

    def get_tax(self):
        tax_total = (18/100) * (self.get_total_price())
        return tax_total
    
    def get_grand_total(self):
        grand_total = self.get_total_price() + self.get_tax()
        return grand_total

class Wishlistitems(TimeStampBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return '{}'.format(self.user)
    
class Payment(TimeStampBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    transaction_id = models.TextField()
    payment_status = models.IntegerField(default=2, choices=PAYMENT_STATUS_CHOICES)

    def __str__(self):
        return '{}'.format(self.transaction_id)
        
