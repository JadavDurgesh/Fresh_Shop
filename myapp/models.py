from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=8)
    otp = models.IntegerField(default=1234)
    
    
    def __str__(self):
        return self.email

class Contact_us(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField()
    subject = models.CharField(max_length=15)
    message = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.name
    
class Categories(models.Model):
    name = models.CharField(max_length=15)    
    
    def __str__(self):
        return self.name
    
class sub_categories(models.Model):
    c_id = models.ForeignKey(Categories,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name  
    
class Add_product(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    categories_id = models.ForeignKey(Categories,on_delete=models.CASCADE)
    s_id = models.ForeignKey(sub_categories,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    offer = models.IntegerField()
    qty = models.IntegerField()
    gram = models.CharField(max_length=50)
    pic = models.ImageField(upload_to="img")
    dis = models.TextField()    
    
    def __str__(self):
        return self.name
    
class Add_to_cart(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    qty = models.IntegerField()
    pic = models.ImageField(upload_to="img")
    total_price = models.IntegerField()    
    
class Address(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)   
    user_name = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()
    address_2 = models.TextField()
    country = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    pincode = models.IntegerField()
    list = models.TextField()
    
class Wishlist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Add_product,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    pic = models.ImageField(upload_to="img")
    
class Order(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    qty = models.IntegerField()
    price = models.IntegerField()
    
    
    def __str__(self):
        return self.name

class G_categories(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
    
class G_subcategories(models.Model):
    c_id = models.ForeignKey(G_categories,on_delete=models.CASCADE)    
    name = models.CharField(max_length=30)
    pic = models.ImageField(upload_to='img')
    
    def __str__(self):
        return self.name
    
    
    
    
        
          
    
    
    
    
    
        
    