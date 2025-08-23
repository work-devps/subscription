from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Feature(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Plan(models.Model):
    name = models.CharField(max_length=100)
    features = models.ManyToManyField(Feature, related_name='plans')
    
    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Ensure only one active subscription per user
        if self.is_active:
            Subscription.objects.filter(user=self.user, is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"