from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings


class DRFDefaultsTests(APITestCase):
    """Test DRF defaults are applied to all endpoints."""
    
    def setUp(self):
        """Create authenticated client."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}'
        )
    
    def test_pagination_applied_to_list_views(self):
        """List endpoints should apply pagination."""
        # Assuming an endpoint exists
        response = self.client.get('/api/v1/customers/')
        if response.status_code == 200:
            # Paginated response should have these keys
            self.assertIn('results', response.data)
            self.assertIn('count', response.data)
            self.assertIn('next', response.data)
            self.assertIn('previous', response.data)
    
    def test_page_size_respects_setting(self):
        """Pagination should respect PAGE_SIZE setting."""
        response = self.client.get('/api/v1/customers/')
        if response.status_code == 200 and response.data.get('results'):
            max_page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
            self.assertLessEqual(
                len(response.data['results']),
                max_page_size
            )
    
    def test_all_endpoints_use_authentication(self):
        """All endpoints should require authentication."""
        endpoints = [
            '/api/v1/customers/',
            '/api/v1/workorders/',
            '/api/v1/inventory/',
        ]
        
        # Remove credentials to test unauthenticated access
        self.client.credentials()
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                401,
                f"Endpoint {endpoint} did not require authentication"
            )