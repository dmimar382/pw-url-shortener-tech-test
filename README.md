## Project Overview
This project implements a URL Shortener web service that allows users to shorten URLs and later resolve them using a shortened version. The service exposes two main API endpoints:

* POST `/url/shorten`: accepts a URL to shorten (e.g. https://www.google.com) and returns a short URL that 
  can be resolved at a later time (e.g. http://localhost:8000/r/abc)
* GET `r/<short_url>`: resolve the given short URL (e.g. http://localhost:8000/r/abc) to its original URL
  (e.g. https://www.google.com). If the short URL is unknown, an HTTP 404 response is returned.

The service is designed to run with multiple workers, ensuring that you can shorten a URL on one instance and resolve it on another.

## Design Decisions: Using a Library for URL Shortening Logic

### Why I Refactored the Logic into a Library

To improve **reusability** and **separation of concerns**, I extracted the core URL shortening logic into a dedicated Python library (`url_shortener.py`). This allows for the business logic to be cleanly decoupled from the FastAPI web service itself, making the codebase easier to maintain, extend, and test.

Key reasons for using a library-based architecture:

1. **Separation of Concerns**: The URL shortening logic is isolated from the API layer. This separation allows for the business logic to be tested and reused independently from the API infrastructure.
2. **Reusability**: The URL shortening library can be used in other contexts (e.g. another service) without needing to rewrite the core logic.
3. **Scalability**: By decoupling the logic, it can be invoked in different ways (e.g., via gRPC or other HTTP-based services), making it scalable for future enhancements.
4. **Easier Testing**: The URL shortening logic can be unit tested separately, making it easier to write comprehensive tests.

### How the Library is Invoked in the API

The `URLShortener` class, implemented in `lib/url_shortener.py`, encapsulates the core functionality, including generating and resolving shortened URLs. This class is instantiated in the FastAPI application and then used to handle incoming requests.

Here is how the library is used:

1. **Library Structure**: 
   - The URL shortening logic is implemented in the `URLShortener` class in the `lib/url_shortener.py` file.
   - The class handles generating Base62-encoded short URLs and storing/retrieving data from MongoDB and Redis.

2. **Integration with FastAPI**:
   - In `server.py`, the FastAPI application initializes the `URLShortener` class. Redis and MongoDB clients are passed into this class, ensuring the service can cache URLs and persist them.
   - The API routes (`/url/shorten` and `/r/{short_url}`) delegate the shortening and resolving tasks to the `URLShortener` library.


## Getting Started
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dmimar382/pw-url-shortener-tech-test.git
   cd pw-url-shortener-tech-test
   ```

2. **Set Up Environment Variables**:
   Copy the contents of the .env.example file located in the deploy folder into a new .env file in the same directory.
   ```bash
   cp deploy/.env.example deploy/.env
   ```

3. **Run the Service with Docker**:
   Use the following command to build and run the service in a Docker container:
   ```bash
   make up
   ```

4. **Access the Service**:
   The service will be running on `http://localhost:8000`. You can access the API documentation via [Swagger UI](http://localhost:8000/docs).

---