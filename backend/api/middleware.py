from backend.core.logger import logger
from backend.core.context import request_id_ctx_var
from backend.core.exceptions import AppError
import uuid
import grpc

class GlobalGrpcInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        handler = continuation(handler_call_details)
        if handler is None:
            return None
            
        def wrapper(request, context):
            # Extract request ID from metadata
            metadata = dict(context.invocation_metadata())
            request_id = metadata.get('x-request-id', str(uuid.uuid4()))
            
            # Set context variable
            token = request_id_ctx_var.set(request_id)
            
            try:
                logger.info(f"Processing request: {handler_call_details.method}")
                return handler.unary_unary(request, context)
            except AppError as e:
                logger.warning(f"Domain Error: {e.code} - {e.message}")
                context.set_trailing_metadata((("x-error-code", e.code),))
                context.abort(e.grpc_status, e.message)
            except Exception as e:
                logger.error(f"Unhandled Exception: {e}", exc_info=True)
                context.set_trailing_metadata((("x-error-code", "INTERNAL_ERROR"),))
                context.abort(grpc.StatusCode.INTERNAL, "An unexpected internal error occurred.")
            finally:
                # Reset context to prevent leakage
                request_id_ctx_var.reset(token)

        return grpc.unary_unary_rpc_method_handler(
            wrapper,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer
        )
