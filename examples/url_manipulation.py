"""
URL manipulation examples for WebUtils.
"""

from webutils import URL, URLBuilder, URLFactory

# Using URL class
print("=== Using URL class ===")
url = URL("https://api.example.com/api/v1/users")
print(f"Hostname: {url.hostname}")
print(f"Path: {url.path}")
print(f"Name: {url.name}")
print(f"Stem: {url.stem}")
print(f"Suffix: {url.suffix}")
print(f"Parent: {url.parent}")

# Join paths
new_url = url / "123"
print(f"Joined: {new_url}")

# Modify URL components
url = url.with_scheme("http")
url = url.with_query(page=1, limit=10)
url = url.with_fragment("section")
print(f"Modified: {url}")

# Add/remove query parameters
url = url.add_param("search", "python")
print(f"Added param: {url}")
url = url.remove_param("page")
print(f"Removed param: {url}")

# Using URLBuilder
print("\n=== Using URLBuilder ===")
url = (URLBuilder()
       .with_url("https://api.example.com")
       .with_endpoint("api/v1/users")
       .with_query(page=1, limit=10)
       .with_fragment("section")
       .build())
print(f"Built URL: {url}")

# Using URLFactory
print("\n=== Using URLFactory ===")
url = URLFactory.from_components(
    scheme="https",
    netloc="api.example.com",
    path="/api/v1/users",
    query="page=1&limit=10"
)
print(f"Factory URL: {url}")
