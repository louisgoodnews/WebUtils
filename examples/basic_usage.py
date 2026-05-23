"""
Basic usage examples for WebUtils.
"""

from webutils import get, post, HTTPService, configure

# Configure default timeout and retry settings
configure(timeout=30.0, max_retries=3, retry_delay=1.0)

# Using top-level convenience functions
print("=== Using convenience functions ===")
response = get("https://httpbin.org/get")
print(f"Status: {response.status}")
print(f"Duration: {response.duration}s")

response = post("https://httpbin.org/post", data={"name": "Test", "value": 123})
print(f"Status: {response.status}")
print(f"Body: {response.body}")

# Using HTTPService class
print("\n=== Using HTTPService class ===")
response = HTTPService.get("https://httpbin.org/get")
print(f"Status: {response.status}")
print(f"Type: {response.type}")
print(f"Success: {response.success()}")
