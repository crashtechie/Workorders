FROM node:20-alpine AS builder

WORKDIR /app
COPY . .

# Build React assets when source is present, or reuse prebuilt assets if available.
RUN set -eux; \
        mkdir -p /out; \
        if [ -f package.json ]; then \
            npm ci; \
            npm run build; \
            if [ -d build ]; then \
                cp -a build/. /out/; \
            elif [ -d dist ]; then \
                cp -a dist/. /out/; \
            else \
                echo "Build finished but no build/ or dist/ directory was produced."; \
                exit 1; \
            fi; \
        elif [ -d build ]; then \
            cp -a build/. /out/; \
        elif [ -d dist ]; then \
            cp -a dist/. /out/; \
        else \
            echo "No React source or prebuilt assets found; creating placeholder page."; \
            printf '%s\n' '<!doctype html><html><head><meta charset="utf-8"><title>Frontend Not Configured</title></head><body><h1>Frontend assets not found</h1></body></html>' > /out/index.html; \
        fi

FROM nginx:1.27-alpine

RUN apk update && apk upgrade --no-cache
COPY --from=builder /out/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN printf '%s\n' '<!doctype html><html><head><meta charset="utf-8"><title>healthy</title></head><body>ok</body></html>' > /usr/share/nginx/html/healthz.html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
        CMD wget --no-verbose --tries=1 --spider http://localhost/healthz || exit 1

CMD ["nginx", "-g", "daemon off;"]
