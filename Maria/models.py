from django.db import models

from django.contrib.auth.models import AbstractUser

from django.utils import timezone

from random import randint

class User(AbstractUser):

    phone=models.CharField(max_length=15,unique=True)

    is_verified=models.BooleanField(default=False)

    otp=models.CharField(max_length=10,null=True)

    def generate_otp(self):

        self.otp=str(randint(1000,9999))

        self.save()

class BaseModel(models.Model):

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class Category(BaseModel):

    name=models.CharField(max_length=80,unique=True)

    def __str__(self):
        return self.name
    
class Size(BaseModel):

    name=models.CharField(max_length=70,unique=True)

    def __str__(self):
        
        return self.name    
    
class Color(BaseModel):

    name=models.CharField(max_length=10)

    def __str__(self):

        return self.name


    
class Dress(BaseModel):

    title=models.CharField(max_length=100)

    description=models.TextField()

    picture=models.ImageField(upload_to="dressimages",null=True,blank=True)

    color_objects=models.ManyToManyField(Color)

    category_objects=models.ManyToManyField(Category)

    def __str__(self):
        
        return self.title
    

class DressVarient(BaseModel):

    dress_object=models.ForeignKey(Dress,on_delete=models.CASCADE,related_name="varients")

    size_object=models.ForeignKey(Size,on_delete=models.CASCADE)

    price=models.FloatField()    

    def __str__(self):
        return self.dress_object.dress.title
    


    
    
class Cart(BaseModel):

    dress_varient_object=models.ForeignKey(DressVarient,on_delete=models.Case)

    color_object=models.ForeignKey(Color,on_delete=models.CASCADE)

    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField()

    is_order_placed=models.BooleanField(default=False)

    def item_total(self):

        return self.quantity*self.dress_varient_object.price    
    
class Order(BaseModel):

    customer=models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    address=models.TextField(null=False, blank=False)

    phone=models.CharField(max_length=20, null=False, blank=False)
    
    PAYMENT_OPTIONS=(
        ("COD","COD"),
        ("ONLINE","ONLINE")
    )

    payment_method=models.CharField(max_length=15, choices=PAYMENT_OPTIONS, default="COD")

    rzp_order_id=models.CharField(max_length=100, null=True)

    is_paid=models.BooleanField(default=False)

    def order_total(self):

        total=0

        order_items=self.orderitems.all()

        if order_items:

            total=sum([oi.item_total() for oi in order_items])

        return total

class OrderItem(BaseModel):

    order_object=models.ForeignKey(Order,on_delete=models.CASCADE, related_name="orderitems")

    dress_varient_object=models.ForeignKey(DressVarient, on_delete=models.CASCADE)
    
    quantity=models.PositiveIntegerField(default=1)
    
    price=models.FloatField()        

    def item_total(self):

        return self.price*self.quantity


