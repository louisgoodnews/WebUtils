# WebUtils

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A lightweight, asynchronous HTTP client library for Python that simplifies making web requests with a clean, intuitive API.

## Features

- 🚀 **Fully Asynchronous**: Built on top of `aiohttp` for high-performance HTTP requests
- 🔄 **Multiple HTTP Methods**: Supports GET, POST, PUT, DELETE, PATCH, and more
- 🔒 **Built-in Authentication**: Supports various auth methods including Basic, Bearer, OAuth, and custom schemes
- 📦 **Response Handling**: Automatic JSON parsing and type conversion
- ⏱️ **Request Timing**: Built-in timing metrics for performance monitoring
- 🛡️ **Error Handling**: Comprehensive error handling and status code management
- 🔗 **URL Manipulation**: pathlib-like URL class for intuitive URL construction and manipulation
- 📝 **Query Parameter Management**: URLQuery class for automated query parameter building and management
- 🧪 **Tested**: Includes unit tests for reliability

## Installation

```bash
pip install webutils-louisgoodnews
```

## Quick Start

```python
from webutils import HTTPService, HTTPMethod, HTTPResponseType

# Make a GET request
response = HTTPService.get("https://api.example.com/data")
print(response.body)  # Access response data
print(response.status)  # HTTP status code
print(response.duration)  # Request duration in seconds

# Make a POST request with JSON data
response = HTTPService.post(
    "https://api.example.com/items",
    data={"name": "New Item", "value": 42}
)
```

## URL Query Parameters

```python
from webutils import URLQuery, URLQueryFactory, URLQueryBuilder

# Using URLQuery directly
query = URLQuery(params={"key": "value", "page": "1"})
print(str(query))  # "key=value&page=1"

# Add multiple values to the same parameter
query.add("tag", "python")
query.add("tag", "web")
print(str(query))  # "key=value&page=1&tag=python&tag=web"

# Using URLQueryBuilder for fluent API
query = (URLQueryBuilder()
         .add_param("key", "value")
         .add_param("page", "1")
         .build())

# Using URLQueryFactory
query = URLQueryFactory.from_url("https://example.com?key=value&page=1")
print(query.get_first("key"))  # "value"
print(query.get_first("page"))  # "1"

# Using URLBuilder with URLQuery
from webutils import URLBuilder

url = (URLBuilder("https://api.example.com")
       .with_endpoint("search")
       .with_query(q="python", page=1)
       .build())
print(str(url))  # "https://api.example.com/search?q=python&page=1"
```

## Authentication

```python
from webutils import Authorization

# Basic Auth
auth = Authorization(username="user", password="pass")
headers = auth.header("basic")  # Returns {'Authorization': 'Basic dXNlcjpwYXNz'}

# Bearer Token
auth = Authorization(username="", password="your_token_here")
headers = auth.header("bearer")  # Returns {'Authorization': 'Bearer your_token_here'}
```

## Response Object

The `HTTPResponse` object provides easy access to response data:

```python
response = HTTPService.get("https://api.example.com/data")

# Access response properties
print(response.status)     # HTTP status code (e.g., 200)
print(response.message)    # Status message (e.g., 'OK')
print(response.body)       # Parsed response body (dict for JSON, str otherwise)
print(response.headers)    # Response headers
print(response.duration)   # Request duration in seconds
print(response.success())  # True if status code is 2xx
```

## Advanced Usage

### Custom Headers

```python
headers = {
    "Content-Type": "application/json",
    "X-Custom-Header": "value"
}
response = HTTPService.get("https://api.example.com/data", headers=headers)
```

### Query Parameters

```python
from webutils import URLBuilder

url = URLBuilder("https://api.example.com/search")
url.add_param("q", "python")
url.add_param("page", 1)

response = HTTPService.get(str(url))
```

## Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/louisgoodnews/WebUtils.git
   cd WebUtils
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

### Running Tests

```bash
pytest
```

### Code Style

This project uses `black` for code formatting and `flake8` for linting:

```bash
black src tests
flake8 src tests
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Louis Goodnews - [@louisgoodnews](https://github.com/louisgoodnews) - louisgoodnews95@gmail.com

Project Link: [https://github.com/louisgoodnews/WebUtils](https://github.com/louisgoodnews/WebUtils)
