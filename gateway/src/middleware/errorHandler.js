/**
 * Global Error Handling Middleware
 * Maps gRPC status codes to HTTP status and Standardized JSON Error.
 */
const errorHandler = (err, req, res, next) => {
    // console.error("Global Error Handler Caught:", err);

    let statusCode = 500;
    let errorCode = "INTERNAL_ERROR";
    let message = "An unexpected error occurred";
    let details = {};

    // 1. Check for gRPC Metadata (x-error-code)
    if (err.metadata) {
        const metaCode = err.metadata.get('x-error-code');
        if (metaCode && metaCode.length > 0) {
            errorCode = metaCode[0];
        }
    }

    // 2. Map gRPC Status Code to HTTP Status
    // https://grpc.github.io/grpc/core/md_doc_statuscodes.html
    if (err.code !== undefined) {
        switch (err.code) {
            case 3: // INVALID_ARGUMENT
                statusCode = 400;
                errorCode = errorCode === "INTERNAL_ERROR" ? "INVALID_ARGUMENT" : errorCode;
                break;
            case 5: // NOT_FOUND
                statusCode = 404;
                errorCode = errorCode === "INTERNAL_ERROR" ? "NOT_FOUND" : errorCode;
                break;
            case 6: // ALREADY_EXISTS
                statusCode = 409;
                errorCode = errorCode === "INTERNAL_ERROR" ? "ALREADY_EXISTS" : errorCode;
                break;
            case 7: // PERMISSION_DENIED
                statusCode = 403;
                break;
            case 16: // UNAUTHENTICATED
                statusCode = 401;
                break;
            case 14: // UNAVAILABLE
                statusCode = 503;
                message = "Service unavailable, please try again later";
                break;
            default:
                statusCode = 500;
        }
    }

    // Use error message from backend if available and safe
    if (err.details) {
        message = err.details;
    }

    // 3. Send Response
    res.status(statusCode).json({
        error: {
            code: errorCode,
            message: message,
            requestId: req.headers['x-request-id'] || "unknown",
            details: details
        }
    });
};

module.exports = errorHandler;
