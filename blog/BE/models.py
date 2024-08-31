from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(5)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
