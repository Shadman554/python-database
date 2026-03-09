"""
Custom middleware for the application
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from time import time
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio
from logger import log_request, log_error, log_security_event

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all HTTP requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time()
        
        # Log request
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"
        
        try:
            response = await call_next(request)
            duration = time() - start_time
            
            # Log response
            log_request(method, path, response.status_code, duration)
            
            # Add custom headers
            response.headers["X-Process-Time"] = str(duration)
            
            return response
            
        except Exception as e:
            duration = time() - start_time
            log_error(e, f"{method} {path}")
            
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error", "path": path}
            )

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware — limits requests per IP address.
    Auth-sensitive endpoints (login, register, google-login) use a much tighter
    limit to prevent brute-force and credential-stuffing attacks.
    """

    # Sensitive auth paths get a stricter per-IP limit (requests per minute)
    AUTH_RATE_LIMIT = 10
    AUTH_PATHS = {
        "/api/auth/login",
        "/api/auth/register",
        "/api/auth/google-login",
        "/api/auth/google-register",
        "/api/auth/refresh",
    }

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)       # general bucket  key=(ip)
        self.auth_requests = defaultdict(list)  # auth bucket     key=(ip)
        self.cleanup_interval = 60
        self.last_cleanup = time()

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks and static docs
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        current_time = time()
        cutoff_time = current_time - 60

        # Periodic cleanup
        if current_time - self.last_cleanup > self.cleanup_interval:
            await self._cleanup_old_entries()
            self.last_cleanup = current_time

        path = request.url.path
        is_auth_path = path in self.AUTH_PATHS

        if is_auth_path:
            auth_times = self.auth_requests[client_ip]
            auth_times[:] = [t for t in auth_times if t > cutoff_time]
            if len(auth_times) >= self.AUTH_RATE_LIMIT:
                log_security_event(
                    "Auth rate limit exceeded",
                    {"ip": client_ip, "path": path}
                )
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Too many authentication attempts. Please try again later.",
                        "retry_after": 60
                    },
                    headers={"Retry-After": "60"}
                )
            auth_times.append(current_time)

        # General rate limit
        request_times = self.requests[client_ip]
        request_times[:] = [t for t in request_times if t > cutoff_time]

        if len(request_times) >= self.requests_per_minute:
            log_security_event(
                "Rate limit exceeded",
                {"ip": client_ip, "path": path}
            )
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "retry_after": 60
                },
                headers={"Retry-After": "60"}
            )

        request_times.append(current_time)

        response = await call_next(request)

        # Add rate limit headers
        remaining = self.requests_per_minute - len(request_times)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        response.headers["X-RateLimit-Reset"] = str(int(current_time + 60))

        return response
    
    async def _cleanup_old_entries(self):
        """Remove old IP entries to prevent memory bloat"""
        current_time = time()
        cutoff_time = current_time - 120  # Keep last 2 minutes

        for bucket in (self.requests, self.auth_requests):
            ips_to_remove = []
            for ip, times in bucket.items():
                times[:] = [t for t in times if t > cutoff_time]
                if not times:
                    ips_to_remove.append(ip)
            for ip in ips_to_remove:
                del bucket[ip]

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Allow Swagger UI resources for API documentation
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https://fastapi.tiangolo.com; "
                "font-src 'self' https://cdn.jsdelivr.net"
            )
        else:
            response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.

    In production (DEBUG=False):
      - 5xx HTTPExceptions have their detail replaced with a generic message
        so internal error strings are never sent to clients.
      - Unhandled exceptions are caught and return a generic 500.
    In development (DEBUG=True):
      - Full error detail is preserved for easier debugging.
    """

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            # Sanitize 5xx responses in production
            try:
                from config import settings as _settings
                is_debug = _settings.DEBUG
            except Exception:
                is_debug = False

            if exc.status_code >= 500 and not is_debug:
                log_error(exc, f"HTTP {exc.status_code} in {request.url.path}")
                return JSONResponse(
                    status_code=exc.status_code,
                    content={"detail": "An internal server error occurred."}
                )
            raise
        except Exception as e:
            # Log unexpected errors
            log_error(e, f"Unhandled error in {request.url.path}")

            # Return generic error response (never expose exception message)
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "An unexpected error occurred",
                    "type": "internal_server_error",
                }
            )
