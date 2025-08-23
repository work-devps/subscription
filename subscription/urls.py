from django.urls import path
from .views import (
    FeatureCreateAPIView,
    FeatureListAPIView,
    PlanCreateAPIView,
    PlanListAPIView,
    SubscriptionCreateAPIView,
    SubscriptionListAPIView,
    SubscriptionUpdateAPIView,
    SubscriptionDeactivateAPIView,
)

app_name = 'subscriptions'

urlpatterns = [
    # Feature endpoints
    path('features/', FeatureListAPIView.as_view(), name='feature-list'),
    path('features/create/', FeatureCreateAPIView.as_view(), name='feature-create'),
    
    # Plan endpoints
    path('plans/', PlanListAPIView.as_view(), name='plan-list'),
    path('plans/create/', PlanCreateAPIView.as_view(), name='plan-create'),
    
    # Subscription endpoints
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscription-list'),
    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
    path('subscriptions/update/', SubscriptionUpdateAPIView.as_view(), name='subscription-update'),
    path('subscriptions/deactivate/', SubscriptionDeactivateAPIView.as_view(), name='subscription-deactivate'),
]