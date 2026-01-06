FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (needed for psycopg2)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy Requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY backend ./backend
COPY proto ./proto

# Install grpc-tools for generation
RUN pip install grpcio-tools

# Generate Proto code
RUN mkdir -p /app/backend/generated
RUN python -m grpc_tools.protoc -I/app/proto --python_out=/app/backend/generated --grpc_python_out=/app/backend/generated /app/proto/library.proto

# Set PYTHONPATH
ENV PYTHONPATH=/app:/app/backend/generated

# Copy entrypoint script
COPY backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 50051

ENTRYPOINT ["/entrypoint.sh"]
