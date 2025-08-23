from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
from .models import Subscription, Plan, Feature
from .serializers import (
    PlanCreateSerializer,
    SubscriptionListSerializer, 
    SubscriptionCreateSerializer,
    SubscriptionUpdateSerializer,
    PlanSerializer,
    FeatureSerializer
)

class FeatureCreateAPIView(generics.CreateAPIView):
    """Create a new feature"""
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticated]

class FeatureListAPIView(generics.ListAPIView):
    """List all features"""
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticated]
    queryset = Feature.objects.all()

class PlanCreateAPIView(generics.CreateAPIView):
    """Create a new plan"""
    serializer_class = PlanCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.save()
        # Return the complete plan with features
        plan_data = PlanSerializer(plan).data
        return Response(plan_data, status=status.HTTP_201_CREATED)

class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Create a new subscription for the authenticated user"""
    serializer_class = SubscriptionCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Deactivate any existing active subscriptions
        Subscription.objects.filter(user=self.request.user, is_active=True).update(is_active=False)
        serializer.save(user=self.request.user)


class SubscriptionListAPIView(generics.ListAPIView):
    """List all subscriptions of the authenticated user with optimized queries"""
    serializer_class = SubscriptionListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)\
            .select_related('plan')\
            .prefetch_related(
                Prefetch('plan__features', queryset=Feature.objects.all())
            ).order_by('-start_date')


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """Change user's plan (creates new subscription and deactivates old one)"""
    serializer_class = SubscriptionUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user, is_active=True)
    
    def get_object(self):
        try:
            return self.get_queryset().get()
        except Subscription.DoesNotExist:
            return None
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {"detail": "No active subscription found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_subscription = serializer.save()
        
        # Return the new subscription data
        return Response(
            SubscriptionListSerializer(new_subscription).data,
            status=status.HTTP_200_OK
        )

class SubscriptionDeactivateAPIView(generics.GenericAPIView):
    """Deactivate user's current subscription"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user, is_active=True)
    
    def post(self, request, *args, **kwargs):
        active_subscription = self.get_queryset().first()
        if not active_subscription:
            return Response(
                {"detail": "No active subscription found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        active_subscription.is_active = False
        active_subscription.save()
        
        return Response(
            {"detail": "Subscription deactivated successfully"},
            status=status.HTTP_200_OK
        )

# Additional view for listing available plans
class PlanListAPIView(generics.ListAPIView):
    """List all available plans with features"""
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Plan.objects.prefetch_related('features').all()