# Full-Stack Library Management System (POC)

A modern, highly-normalized Library Management System built with a **Python gRPC Backend**, **NodeJS API Gateway**, and **React (Vite) Frontend**. This project demonstrates advanced database normalization (3NF), centralized error handling (AOP), and containerized microservices.

## 🏗️ Architecture

```mermaid
graph TD
    UI[React Frontend] -->|REST| GW[NodeJS API Gateway]
    GW -->|gRPC| BE[Python gRPC Backend]
    BE -->|SQLAlchemy| DB[(PostgreSQL)]
```

### Key Technical Highlights
- **Normalized Schema**: Distinct entities for `Authors`, `Genres`, `BookMetadata`, and `BookCopies` to ensure data integrity and zero redundancy.
- **SOLID Design Principles**: 
    - **Single Responsibility (SRP)**: Logic is strictly decoupled into Repository (Data), Manager (Business), and Service (API) layers.
    - **Open/Closed (OCP)**: The validation system (e.g., `ILoanValidator`) allows new rules to be added without modifying existing code.
    - **Dependency Inversion (DIP)**: High-level business logic depends on abstractions rather than low-level database implementations.
- **Advanced OOP Implementation**: Intensive use of Classes, Abstract Base Classes (ABC), and Encapsulation to manage complex business domains.
- **Cross-Cutting Concerns (AOP)**: 
    - **Centralized Exception Handling**: A Global gRPC Interceptor catches backend exceptions, maps them to domain errors, and sends them to the Gateway, where a centralized Middleware ensures a consistent JSON error contract.
    - **Distributed Tracing**: Implements End-to-End request tracking. A UUID generated at the Frontend/Gateway is propagated through gRPC metadata to the Backend logs, ensuring complete observability across microservices.
        - **Log Format**: `[uuid] [service_name] [timestamp] [level] [module.function] message`
- **Global Automatic Transaction Management**: Implements the **Unit of Work** pattern via a custom `db_scope`. Transactions are automatically committed on success and rolled back on failure (ACID compliance), simplifying service logic and preventing data inconsistencies.
- **Microservices Architecture**: Fully Dockerized stack with bridge networking and automated service-to-service orchestration.
- **Modern Frontend Architecture**:
    - **Vite & React 18**: Leveraging the fastest build tools and modern React patterns.
    - **Centralized Service Layer**: Decoupled HTTP logic from UI components using an API repository pattern.
    - **Centralized Service Layer**: Decoupled HTTP logic from UI components using an API repository pattern.
    - **Utility-First Styling**: Consistent, responsive UI built with Tailwind CSS.
- **Production-Grade Database Pooling**: Implements explicit SQLAlchemy `QueuePool` configuration with connection recycling to prevent stale connections and ensure performance under load.

---

## 🛠️ Configuration
The application uses industry-standard defaults for database connection pooling, which can be overridden via environment variables:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `POSTGRES_POOL_SIZE` | `5` | Number of connections to keep open. |
| `POSTGRES_MAX_OVERFLOW` | `10` | Max temporary connections during spikes. |
| `POSTGRES_POOL_TIMEOUT` | `30` | Seconds to wait for a connection before timeout. |
| `POSTGRES_POOL_RECYCLE` | `1800` | Seconds before recycling a connection (30m). |

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

1.  **Docker Desktop** (Version 20.10.0 or higher)
2.  **Docker Compose** (Version 2.0.0 or higher)

*No local Python, NodeJS, or PostgreSQL installation is required as everything runs inside containers.*

---

## 🚀 How to Run

Follow these steps to spin up the entire application stack:

### 1. Extract & Navigate
1.  Extract the provided `.zip` file to your preferred directory.
2.  Open a terminal and navigate to the extracted `poc` folder:
    ```bash
    cd path/to/extracted/poc
    ```

### 2. Launch & Seed
Run the following command to build, start, and automatically seed the application:
```bash
docker compose up -d
```
*Wait ~45 seconds. The system will automatically initialize the database and load the unique sample dataset.*

### 3. Running Backend Tests (Optional)
The system supports running a full test suite with coverage reporting before the application boots. This is disabled by default but can be enabled via the `RUN_TESTS` environment variable:

**Run Tests with Coverage Report:**
You can run the full test suite and generate a coverage report at any time using the following command inside the backend container (or locally):
```bash
pytest --cov=backend tests/
```
**Current Status**: The project has achieved **91% Test Coverage**, ensuring high reliability across Controllers, Services, and Repositories.

---

## 🌐 Component Access

Once the stack is running, you can access the components at the following URLs:

| Component | URL | Description |
| :--- | :--- | :--- |
| **Frontend UI** | [http://localhost:5173](http://localhost:5173) | Main dashboard for library operations. |
| **API Gateway** | [http://localhost:3001](http://localhost:3001) | RESTful entry point for external integrations. |
| **Backend gRPC** | `localhost:50051` | The core business logic layer. |

---

## 🧪 Exploration & Testing

### 1. Advanced Normalization
- Navigate to the **Add Book** form.
- Select from the pre-seeded **Authors** and multiple **Genres**.
- Add physical copies to see the `Available / Total` stock counts update in real-time.

### 2. Validation & Error Handling
- Attempt to create a member with an existing email (`alice.j@example.com`).
- Attempt to add a book with an existing ISBN.
- Observe the specific error messages propagated from the backend through the AOP interceptor.

## 🛠️ Internal Structure
- `backend/`: Python server using SQLAlchemy and gRPC.
- `gateway/`: NodeJS/Express server using `@grpc/grpc-js`.
- `frontend/`: React application using Vite and Tailwind CSS.
- `proto/`: Centralized `.proto` definitions for the entire stack.
