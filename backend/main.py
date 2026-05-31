# Minimal Django health check stub for container readiness.
# This satisfies the Docker HEALTHCHECK before the full Django project
# is scaffolded. Runs Django's development server on port 8080.
# Not for production use — replace with gunicorn + full project entrypoint.
import os
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        ALLOWED_HOSTS=["*"],
        ROOT_URLCONF=__name__,
        SECRET_KEY=os.environ.get("DJANGO_SECRET_KEY", "placeholder-change-before-production"),
    )

django.setup()

from django.http import JsonResponse  # noqa: E402
from django.urls import path  # noqa: E402


def health_check(request):
    return JsonResponse({"status": "healthy"})


urlpatterns = [
    path("health", health_check),
]

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8080", "--noreload"])