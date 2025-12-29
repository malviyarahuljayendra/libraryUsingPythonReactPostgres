FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (needed for psycopg2)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy Requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY backend /app/backend
COPY backend/main.py /app/
COPY proto /app/proto

# Install grpc-tools for generation
RUN pip install grpcio-tools

# Generate Proto code
RUN mkdir -p /app/generated
RUN python -m grpc_tools.protoc -I/app/proto --python_out=/app/generated --grpc_python_out=/app/generated /app/proto/library.proto

# Set PYTHONPATH
ENV PYTHONPATH=/app:/app/generated

EXPOSE 50051

CMD ["python", "main.py"]
