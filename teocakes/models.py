from django.db import models
from django.utils.text import slugify
from django.conf import settings
class Cake(models.Model):
    CATEGORY =(("Wedding","WEDDING"),
               ("Birthday","BIRTHDAY"),
                ("Dessert","DESSERT"),
                 ("Graduation","GRADUATION"),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    description=models.TextField(blank=True,null=True)
    price =models.DecimalField(max_digits=10,decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY,blank=True,null=True)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            unique_slug = self.slug
            counter =1
            while Cake.objects.filter(slug=unique_slug).exists():
                unique_slug =f'{self.slug}-{counter}'
                counter += 1
            self.slug = unique_slug
        
        super().save(*args, **kwargs)
class Cart(models.Model):
    cart_id = models.CharField(max_length=12, blank=False ,unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cakes')
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.cake.name} in cart {self.cart.cart_id}'
    
class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    

  