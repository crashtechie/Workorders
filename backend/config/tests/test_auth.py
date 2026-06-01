from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class JWTAuthenticationTests(APITestCase):
    """Test JWT authentication baseline."""
    
    def setUp(self):
        """Create test user and tokens."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
    
    def test_protected_endpoint_without_token_returns_401(self):
        """Unauthenticated request should return 401."""
        response = self.client.get('/api/v1/customers/')
        self.assertEqual(response.status_code, 401)
    
    def test_protected_endpoint_with_valid_token_returns_200(self):
        """Request with valid JWT token should succeed."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/v1/customers/')
        # May return 200 or other 2xx depending on data
        self.assertLess(response.status_code, 400)
    
    def test_invalid_token_returns_401(self):
        """Request with invalid token should return 401."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid-token')
        response = self.client.get('/api/v1/customers/')
        self.assertEqual(response.status_code, 401)
    
    def test_malformed_auth_header_returns_401(self):
        """Malformed Authorization header should return 401."""
        self.client.credentials(HTTP_AUTHORIZATION='InvalidScheme token')
        response = self.client.get('/api/v1/customers/')
        self.assertEqual(response.status_code, 401)
    
    def test_token_refresh_endpoint(self):
        """Refresh token should work at /token/refresh/ endpoint."""
        response = self.client.post(
            '/api/v1/auth/token/refresh/',
            {'refresh': str(self.refresh)},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)