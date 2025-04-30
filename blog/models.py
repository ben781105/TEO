from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from taggit.managers import TaggableManager
class Post(models.Model):
    CATEGORY = (
        ('cake recipes and baking tips','CAKE RECIPES AND BAKING TIPS'),
        ('celebration ideas','CELEBRATION IDEAS'),
        ('behind the scenes','BEHIND THE SCENES'),
        ('cake design trends','CAKE DESIGN TRENDS'),
        ('customer stories and testimonials','CUSTOMER STORIES AND TESIMONIALS'),
        ('seasonal and holiday specials','SEASONAL AND HOLIDAY SPECIALS'),
    )
    image = models.ImageField(upload_to= 'images/')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=500,unique=True,blank=True,null=True)
    excerpt = models.TextField(blank=True,null=True)
    author = models.CharField(max_length=100,blank=True,null=True)
    content = RichTextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100, choices= CATEGORY,blank=True,null=True)
    tags =TaggableManager(blank=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
from django.db import models

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.name}'

