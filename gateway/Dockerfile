FROM node:18-alpine

WORKDIR /app

COPY gateway/package*.json ./
RUN npm install

# Copy source and proto
COPY gateway .
COPY proto /app/proto

ENV PROTO_PATH=/app/proto/library.proto

EXPOSE 3001

CMD ["npm", "start"]
