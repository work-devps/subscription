from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Feature, Plan, Subscription

User = get_user_model()


class SubscriptionModelTestCase(TestCase):
    def setUp(self):
        # Fresh user for model-only tests
        self.user = User.objects.create_user(
            username=f'testuser_{self._testMethodName}',
            email=f'{self._testMethodName}@example.com',
            password='testpass123'
        )
        self.feature1 = Feature.objects.create(name='Call Support')
        self.feature2 = Feature.objects.create(name='Tech Support')
        self.plan = Plan.objects.create(name='Advanced Plan')
        self.plan.features.add(self.feature1, self.feature2)

    def test_subscription_creation(self):
        """Test subscription creation and auto-deactivation of previous subscriptions"""
        subscription1 = Subscription.objects.create(user=self.user, plan=self.plan)
        self.assertTrue(subscription1.is_active)

        new_plan = Plan.objects.create(name='Simple Plan')
        subscription2 = Subscription.objects.create(user=self.user, plan=new_plan)

        subscription1.refresh_from_db()
        self.assertFalse(subscription1.is_active)
        self.assertTrue(subscription2.is_active)


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        # Fresh user per test for isolation
        self.user = User.objects.create_user(
            username=f'devuser_{self._testMethodName}',
            email=f'{self._testMethodName}@example.com',
            password='admin123'
        )
        self.feature1 = Feature.objects.create(name='Unlimited API Access')
        self.feature2 = Feature.objects.create(name='Priority Support')
        self.plan = Plan.objects.create(name='Pro Plan')
        self.plan.features.add(self.feature1, self.feature2)

        # Authenticate user for API calls
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_subscription_creation_api(self):
        data = {'plan': self.plan.id}
        response = self.client.post('/api/v1/subscriptions/create/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)
        subscription = Subscription.objects.first()
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertTrue(subscription.is_active)

    def test_subscription_list_with_nested_data(self):
        Subscription.objects.create(user=self.user, plan=self.plan)

        response = self.client.get('/api/v1/subscriptions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        # Unwrap pagination
        results = data["results"]

        # Check active subscriptions
        active_subscriptions = [s for s in results if s["is_active"]]
        self.assertEqual(len(active_subscriptions), 1)

        subscription_data = active_subscriptions[0]
        self.assertIn('plan', subscription_data)
        self.assertEqual(subscription_data['plan']['name'], 'Pro Plan')
        self.assertIn('features', subscription_data['plan'])
        self.assertEqual(len(subscription_data['plan']['features']), 2)

        feature_names = [f['name'] for f in subscription_data['plan']['features']]
        self.assertIn('Unlimited API Access', feature_names)
        self.assertIn('Priority Support', feature_names)

    def test_plan_switching(self):
        subscription = Subscription.objects.create(user=self.user, plan=self.plan)

        new_feature = Feature.objects.create(name='Advanced Analytics')
        new_plan = Plan.objects.create(name='Super Enterprise Plan')
        new_plan.features.add(new_feature)

        data = {'plan': new_plan.id}
        response = self.client.put('/api/v1/subscriptions/update/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscription.refresh_from_db()
        self.assertFalse(subscription.is_active)

        new_subscription = Subscription.objects.filter(is_active=True).first()
        self.assertEqual(new_subscription.plan, new_plan)
        self.assertEqual(new_subscription.user, self.user)

    def test_subscription_deactivation(self):
        subscription = Subscription.objects.create(user=self.user, plan=self.plan)
        response = self.client.post('/api/v1/subscriptions/deactivate/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscription.refresh_from_db()
        self.assertFalse(subscription.is_active)

    def test_query_optimization(self):
        Subscription.objects.create(user=self.user, plan=self.plan)
        with self.assertNumQueries(4):  # 1 user, 1 count, 1 subscription+plan, 1 prefetch features
            response = self.client.get('/api/v1/subscriptions/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self):
        self.client.credentials()  # remove auth
        response = self.client.get('/api/v1/subscriptions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
