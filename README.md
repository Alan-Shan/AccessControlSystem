# Access Control System

This project implements an Access Control System using Python, Flask, React, JWT (JSON Web Tokens) for authentication and authorization, Swagger for API documentation (/api/docs/), and Docker Compose for containerization. It includes separate back-end and front-end components, as well as unit tests. 

## Features

- User registration and authentication
- Role-based access control (RBAC)
- Token-based authentication using JWT (refresh and access tokens)
- API endpoints for managing users, roles, and permissions
- Swagger UI for interactive API documentation

## Technologies Used

- Python: Programming language used for the back-end development.
- Flask: Web framework for building the RESTful API.
- React: JavaScript library for building the user interface.
- JWT: JSON Web Tokens for secure authentication and authorization.
- Docker Compose: Tool for defining and running multi-container Docker applications.
- Swagger: API documentation tool with Swagger UI for interactive documentation.
- Unit Testing: Automated tests for ensuring the correctness of the code.

## Getting Started

### Prerequisites

- Docker and Docker Compose should be installed on your machine.

### Installation

1. Clone the repository:

```
git clone <repository-url>
```

2. Navigate to the project directory:

```
cd access-control-system
```

### Configuration

1. Set up the environment variables:

   - Create a `.env` file in the root directory based on the provided `.env.example` file.
   - Modify the values in the `.env` file according to your requirements.

2. Set up the back-end:

   - Navigate to the `backend` directory:

   ```
   cd backend
   ```

   - Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up the front-end:

   - Navigate to the `frontend` directory:

   ```
   cd ../frontend
   ```

   - Install the required dependencies:

   ```
   npm install
   ```

### Usage

1. Start the application using Docker Compose:

```
docker-compose up
```

2. The back-end server will be running on `http://localhost:5000`, and the front-end will be running on `http://localhost:3000`.

3. Access the Swagger UI for API documentation:

   - Open `http://localhost:5000/api/docs/` in your web browser.

### Running Unit Tests

1. To run the unit tests for the back-end, navigate to the `backend` directory:

```
cd backend
```

2. Run the tests using the following command:

```
python -m unittest discover tests
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please create a GitHub issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
