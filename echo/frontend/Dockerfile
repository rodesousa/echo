# Stage 1: Builder
FROM node:20-alpine AS builder

# Install pnpm globally
RUN npm install -g pnpm

WORKDIR /app

# Copy dependency files (pnpm specific)
COPY package.json pnpm-lock.yaml ./

# Install dependencies (includes devDependencies needed for build)
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Set production environment
ENV NODE_ENV=production

# Build arguments for Vite environment variables
ARG VITE_API_BASE_URL
ARG VITE_PARTICIPANT_BASE_URL
ARG VITE_DIRECTUS_PUBLIC_URL
ARG VITE_USE_PARTICIPANT_ROUTER=0
ARG VITE_DISABLE_SENTRY=1

# Expose variables for Vite (build time)
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_PARTICIPANT_BASE_URL=${VITE_PARTICIPANT_BASE_URL}
ENV VITE_DIRECTUS_PUBLIC_URL=${VITE_DIRECTUS_PUBLIC_URL}
ENV VITE_USE_PARTICIPANT_ROUTER=${VITE_USE_PARTICIPANT_ROUTER}
ENV VITE_DISABLE_SENTRY=${VITE_DISABLE_SENTRY}

# Compile i18n messages (lingui)
RUN pnpm run messages:compile

# Build the application
RUN pnpm run build

# Stage 2: Production server
FROM nginx:alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Create nginx user (if not exists) and set permissions
RUN addgroup -g 101 -S nginx 2>/dev/null || true && \
    adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx nginx 2>/dev/null || true

# Copy built assets from builder
COPY --from=builder --chown=nginx:nginx /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create necessary directories and set permissions
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    chmod -R 755 /usr/share/nginx/html

# Switch to non-root user
USER nginx

# Expose port 80
EXPOSE 80

# Healthcheck using curl
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
