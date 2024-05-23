# YATUBE API

YATUBE API is a project that provides RESTful APIs for managing posts, comments, groups, and user subscriptions. It's designed to be a backend system without a frontend interface.

## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:zmlkf/api_for_yatube.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:

    ```bash
    python manage.py migrate
    ```

4. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

### API Endpoints

- `/admin/`: Django admin panel for managing database objects.
- `/api/`: Base endpoint for API.
- `/api/v1/posts/`: Endpoint for managing posts.
- `/api/v1/groups/`: Endpoint for managing groups.
- `/api/v1/posts/{post_id}/comments/`: Endpoint for managing comments on a specific post.
- `/api/v1/follow/`: Endpoint for managing user subscriptions.

### Authentication

Authentication is handled using JSON Web Tokens (JWT). To obtain a token, use the `/auth/jwt/create/` endpoint provided by `djoser.urls.jwt` included in the project. Pass your username and password as a JSON payload to this endpoint to receive a token.

### Redoc

Redoc documentation is available at `/redoc/` endpoint, which provides detailed documentation about the available API endpoints, request parameters, and responses.

## Contributors

- **Roman Zemliakov**: [GitHub](https://github.com/zmlkf)