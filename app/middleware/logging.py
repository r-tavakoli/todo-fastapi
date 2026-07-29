import logging

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        response = await call_next(request)

        logger.info(
            "request_id=%s method=%s path=%s status=%s duration=%.3fs",
            request.state.request_id,
            request.method,
            request.url.path,
            response.status_code,
            request.state.duration,
        )

        return response