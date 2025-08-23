from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Feature, Plan, Subscription

User = get_user_model()

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name']

class PlanSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    feature_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    
    class Meta:
        model = Plan
        fields = ['id', 'name', 'features', 'feature_ids']
    
    def create(self, validated_data):
        feature_ids = validated_data.pop('feature_ids', [])
        plan = Plan.objects.create(**validated_data)
        if feature_ids:
            plan.features.set(feature_ids)
        return plan

class SubscriptionListSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'start_date', 'is_active', 'plan']

class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['plan']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['plan']
    
    def update(self, instance, validated_data):
        # Deactivate current subscription
        instance.is_active = False
        instance.save()
        
        # Create new subscription with new plan
        new_subscription = Subscription.objects.create(
            user=instance.user,
            plan=validated_data['plan'],
            is_active=True
        )
        return new_subscription

class SubscriptionDeactivateSerializer(serializers.Serializer):
    """Serializer for subscription deactivation - no fields needed"""
    pass

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name']

class PlanCreateSerializer(serializers.ModelSerializer):
    feature_ids = serializers.ListField(child=serializers.IntegerField())
    
    class Meta:
        model = Plan
        fields = ['name', 'feature_ids']
    
    def create(self, validated_data):
        feature_ids = validated_data.pop('feature_ids')
        plan = Plan.objects.create(**validated_data)
        plan.features.set(feature_ids)
        return plan

class PlanSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'name', 'features']
        

class SubscriptionListSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'start_date', 'is_active', 'plan']

class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['plan']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['plan']
    
    def update(self, instance, validated_data):
        # Deactivate current subscription
        instance.is_active = False
        instance.save()
        
        # Create new subscription with new plan
        new_subscription = Subscription.objects.create(
            user=instance.user,
            plan=validated_data['plan'],
            is_active=True
        )
        return new_subscription
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user