from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware


class TimingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = perf_counter()

        response = await call_next(request)

        duration = perf_counter() - start

        request.state.duration = duration

        response.headers["X-Process-Time"] = f"{duration:.3f}"

        return response