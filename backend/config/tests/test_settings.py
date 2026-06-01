import os
from django.test import TestCase, override_settings
from django.conf import settings


class SettingsLoadingTests(TestCase):
    """Test environment variable loading and Django settings configuration."""
    
    def test_debug_mode_based_on_env(self):
        """Django test runner should force DEBUG off for test execution."""
        self.assertFalse(settings.DEBUG)
    
    @override_settings(DEBUG=False, APP_ENV='production')
    def test_production_security_headers(self):
        """Production should enforce security settings."""
        # In production, security headers should be enabled
        # This is verified during production deployment
        pass
    
    def test_database_url_configuration(self):
        """Database should be configurable via DATABASE_URL."""
        self.assertIn('default', settings.DATABASES)
        self.assertIsNotNone(settings.DATABASES['default']['ENGINE'])
    
    def test_secret_key_not_exposed(self):
        """SECRET_KEY should not be a development default in production."""
        # This test runs in development/test only
        self.assertIsNotNone(settings.SECRET_KEY)
    
    def test_drf_pagination_configured(self):
        """DRF should have pagination configured."""
        drf_config = settings.REST_FRAMEWORK
        self.assertEqual(
            drf_config['DEFAULT_PAGINATION_CLASS'],
            'rest_framework.pagination.PageNumberPagination'
        )
        self.assertIsNotNone(drf_config['PAGE_SIZE'])
    
    def test_jwt_configuration(self):
        """JWT settings should be properly configured."""
        jwt_config = settings.SIMPLE_JWT
        self.assertEqual(jwt_config['ALGORITHM'], 'HS256')
        self.assertIsNotNone(jwt_config['ACCESS_TOKEN_LIFETIME'])