from contextvars import ContextVar

# Context variable to store the request ID
# Default is None meaning no request context
request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default=None)
