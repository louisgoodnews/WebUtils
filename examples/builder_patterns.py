"""
Builder pattern examples for WebUtils.
"""

from webutils import (
    HTTPResponseBuilder,
    AuthorizationBuilder,
    HeaderBuilder,
    URLBuilder,
    HTTPMethod,
    HTTPResponseType,
)

# Build HTTPResponse
print("=== Building HTTPResponse ===")
response = (HTTPResponseBuilder()
           .with_method(HTTPMethod.GET)
           .with_status(200)
           .with_message("OK")
           .with_type(HTTPResponseType.JSON)
           .with_body({"data": "value"})
           .with_url("https://api.example.com/data")
           .build())
print(f"Response status: {response.status}")
print(f"Response type: {response.type}")

# Build Authorization
print("\n=== Building Authorization ===")
auth = (AuthorizationBuilder()
        .with_username("user")
        .with_password("pass")
        .build())
print(f"Basic auth: {auth.basic()}")

# Build Headers
print("\n=== Building Headers ===")
headers = (HeaderBuilder()
          .with_content_type("application/json")
          .with_accept("application/json")
          .build())
print(f"Headers: {headers}")

# Build URL
print("\n=== Building URL ===")
url = (URLBuilder()
       .with_url("https://api.example.com")
       .with_endpoint("api/v1/users")
       .with_query(page=1, limit=10)
       .build())
print(f"URL: {url}")
