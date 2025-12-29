const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = process.env.PROTO_PATH || path.join(__dirname, '../../proto/library.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});

const libraryProto = grpc.loadPackageDefinition(packageDefinition).library;

const client = new libraryProto.LibraryService(
    process.env.BACKEND_HOST,
    grpc.credentials.createInsecure()
);

module.exports = client;
