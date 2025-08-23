from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField('auth.Group',verbose_name='groups',blank=True,related_name='customuser_set',related_query_name='customuser',)
    user_permissions = models.ManyToManyField('auth.Permission',verbose_name='user permissions',blank=True,related_name='customuser_set',related_query_name='customuser',)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email