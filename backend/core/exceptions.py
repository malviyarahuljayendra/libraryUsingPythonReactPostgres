import grpc

class AppError(Exception):
    """Base class for all application domain exceptions."""
    def __init__(self, message: str, code: str, grpc_status: grpc.StatusCode):
        super().__init__(message)
        self.message = message
        self.code = code
        self.grpc_status = grpc_status

class EntityNotFoundError(AppError):
    def __init__(self, message: str = "Entity not found"):
        super().__init__(message, "NOT_FOUND", grpc.StatusCode.NOT_FOUND)

class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, "ALREADY_EXISTS", grpc.StatusCode.ALREADY_EXISTS)

class ValidationError(AppError):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, "INVALID_ARGUMENT", grpc.StatusCode.INVALID_ARGUMENT)

class DatabaseError(AppError):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, "INTERNAL", grpc.StatusCode.INTERNAL)

# Backward compatibility aliases if needed, but better to migrate
LibraryError = AppError
