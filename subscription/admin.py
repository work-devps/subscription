from django.contrib import admin
from .models import Feature, Plan, Subscription

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    filter_horizontal = ['features']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'plan', 'start_date', 'is_active']
    list_filter = ['is_active', 'start_date', 'plan']
    search_fields = ['user__email', 'user__username', 'plan__name']
    readonly_fields = ['start_date']