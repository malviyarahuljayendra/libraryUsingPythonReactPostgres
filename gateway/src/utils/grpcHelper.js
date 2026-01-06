const grpc = require('@grpc/grpc-js');

/**
 * Wraps a gRPC method call in a Promise for async/await usage.
 * Automatically extracts error details if they exist.
 */
const grpcAsync = (client, method, request, req) => {
    return new Promise((resolve, reject) => {
        // Propagate Request ID
        const metadata = new grpc.Metadata();
        if (req.headers['x-request-id']) {
            metadata.add('x-request-id', req.headers['x-request-id']);
        }

        client[method](request, metadata, (err, response) => {
            if (err) {
                // Attach req for context if needed
                err.req = req;
                return reject(err);
            }
            resolve(response);
        });
    });
};

module.exports = { grpcAsync };
