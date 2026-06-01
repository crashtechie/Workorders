from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView


class ProtectedListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "count": 0,
                "next": None,
                "previous": None,
                "results": [],
            }
        )


def health_check(request):
    return JsonResponse({"status": "healthy"})


urlpatterns = [
    path("api/v1/health/", health_check),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/customers/", ProtectedListView.as_view(), name="customers-list"),
    path("api/v1/workorders/", ProtectedListView.as_view(), name="workorders-list"),
    path("api/v1/inventory/", ProtectedListView.as_view(), name="inventory-list"),
    path("admin/", admin.site.urls),
]
