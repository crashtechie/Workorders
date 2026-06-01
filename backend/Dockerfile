# This Dockerfile is used to build the backend of the application using the uv image from Astral. It sets up the working directory, copies the application code, and updates the Alpine packages.
FROM ghcr.io/astral-sh/uv:alpine3.23

WORKDIR /app

COPY . /app

RUN apk update && apk upgrade --no-cache && apk add --no-cache \
    build-base \
    python3-dev \
    py3-pip \
    py3-uv \
    curl \
    tzdata

RUN uv venv --clear /app/.venv
RUN uv pip install --python /app/.venv/bin/python -r requirements.txt

ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000
EXPOSE 8080
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import sys,urllib.request; sys.exit(0) if urllib.request.urlopen('http://127.0.0.1:8080/api/v1/health/', timeout=3).getcode()==200 else sys.exit(1)" || exit 1

# Container should run with no app configured and will be configured at runtime by the entrypoint script
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080", "--noreload"]