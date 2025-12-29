import grpc
from backend.core.exceptions import LibraryError, EntityNotFoundError, ValidationError, ConflictError

class ExceptionInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        handler = continuation(handler_call_details)
        if handler is None:
            return None

        # Only intercept unary-unary calls for now
        if handler.request_streaming or handler.response_streaming:
            return handler

        def wrapper(request, context):
            try:
                return handler.unary_unary(request, context)
            except EntityNotFoundError as e:
                context.abort(grpc.StatusCode.NOT_FOUND, str(e))
            except ConflictError as e:
                context.abort(grpc.StatusCode.ALREADY_EXISTS, str(e))
            except ValidationError as e:
                context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(e))
            except LibraryError as e:
                context.abort(grpc.StatusCode.INTERNAL, str(e))
            except Exception as e:
                # Log unexpected errors
                print(f"Unhandled Exception in interceptor: {e}")
                import traceback
                traceback.print_exc()
                context.abort(grpc.StatusCode.INTERNAL, "An unexpected error occurred.")

        return grpc.unary_unary_rpc_method_handler(
            wrapper,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer
        )
