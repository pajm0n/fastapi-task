# Recruitment Task

## Prerequisites

-   Docker

Make sure that both Docker  are installed and running on your system. If they are not, please install them by following the official installation guides:

-   [Docker installation](https://docs.docker.com/get-docker/)

## Getting Started

To run the project locally, follow these steps:
    
1.  **Build the Docker image**:
    
    ```
    docker compose build
    
    ```
    
2.  **Start the application**:
    
    ```
    docker compose up
    
    ```
    
3.  **Access the project**:  
    Once the containers are up and running, you can access the project in your browser at:
    
    ```
    http://localhost:8000/docs
    
    ```
    

## Docker Configuration

The provided `Dockerfile` and `docker-compose.yml` files are meant for local development purposes only. 

**Important**: The Docker configuration is not suitable for production environments. Further optimizations and modifications would be necessary to use this setup in production.

## Potential Improvements

This project can be further enhanced in the following ways:

### 1. **GeoJSON Upload Validation**

The current validation is based only on an example. A more comprehensive validation should be implemented to ensure that the uploaded GeoJSON files meet required standards.

### 2. **Geo Data Support in Database**

Since this project deals with geographical data, it would be beneficial to use a database that supports geo-spatial queries (e.g., PostgreSQL with PostGIS).

### 3. **Production-Ready Docker Image**

The Docker setup is currently designed for local development. To make it production-ready, you would need to make optimizations such as multi-stage builds and security improvements.

### 4. **Code Quality Tools**

Consider adding configuration for linters and other code quality tools (e.g., Flake8, Black, or Prettier) to ensure that the code adheres to best practices and is consistent.

### 5. **Modularization**

If the application were to grow, it would be beneficial to refactor the code to make it more modular. This would involve organizing the directory structure to better separate the core functionalities and modules.

### 6. **Architecture Improvement**

The current architecture has been kept simple for the sake of this task (CRUD API). To improve scalability and maintainability, you could introduce more isolated layers and consider more complex architectures (e.g., separating the business logic from data handling, using dto, domain objects etc.).
