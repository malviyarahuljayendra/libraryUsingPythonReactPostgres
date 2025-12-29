# Task Checklist

- [x] Externalize configuration values to property files
    - [x] Create `.env` files for backend and gateway
    - [x] Update backend configuration to read from `.env`
    - [x] Update gateway configuration to read from `.env`
    - [x] Update frontend configuration to use environment variables
    - [x] Create a root `.env` for docker-compose
    - [x] Update client.py to use environment variables
    - [x] Verify changes

- [x] Refactor Database Layer (Deep Granularization)
- [x] Consolidate Repository Layer
    - [x] Move `repositories/` sub-package into `core/database/`
    - [x] Update `backend/core/database/__init__.py` to re-export repositories
    - [x] Update imports in `services/managers/` and `services/validators/`
    - [x] Verify everything

- [x] Implement Update Functionality
    - [x] Update `library.proto` with `UpdateBook` and `UpdateMember`
    - [x] Regenerate gRPC code
    - [x] Add update logic to repositories (Backend)
    - [x] Add update logic to managers (Backend)
    - [x] Implement gRPC update methods in service (Backend)
    - [x] Add `PUT` routes to Gateway
    - [x] Verify end-to-end functionality

- [x] Centralized Error Handling (AOP)
    - [x] Create custom exception hierarchy in `backend/core/exceptions.py`
    - [x] Implement gRPC Server Interceptor for centralized error mapping
    - [x] Update `backend/main.py` to use the interceptor
    - [x] Refactor `backend/api/service.py` to remove redundant try-except blocks
    - [x] Update Managers and Validators to throw custom exceptions
    - [x] Verify error propagation to Gateway and UI

- [x] Advanced Database Normalization
    - [x] Update `proto/library.proto` for Authors, Genres, and Book Metadata
    - [x] Update SQLAlchemy models for the new relational structure
    - [x] Refactor Repositories to handle Authors, Genres, and Copies
    - [x] Update Managers with business logic for normalized entities
    - [x] Update gRPC Service implementations
    - [x] Regenerate gRPC code and update Gateway/Frontend
    - [x] Verify migration and data integrity

- [x] Implement Initial Stock during Book Creation
    - [x] Update `library.proto` with `initial_copies` field
    - [x] Regenerate gRPC code
    - [x] Update `BookManager` to create physical copies
    - [x] Update `LibraryService` gRPC server
    - [x] Update Gateway routes
    - [x] Update `BookForm` UI with 'Copies' field
    - [x] Verify functionality

- [x] Enhanced Validation and Boot Options
    - [x] Implement UI Validation in `BookForm.jsx`
    - [x] Implement UI Validation in `BorrowForm.jsx`
    - [x] Add interactive schema recreation option in `backend`
    - [x] Verify functionality
