"""
Bulk request examples for WebUtils.
"""

from webutils import bulk_get, bulk_post

# Make multiple GET requests concurrently
print("=== Bulk GET requests ===")
urls = ["https://httpbin.org/get", "https://httpbin.org/get"]
try:
    response = bulk_get(urls)
    print(f"Status: {response.status}")
    print(f"Results count: {len(response.body['results'])}")
except Exception as e:
    print(f"Error: {e}")

# Make multiple POST requests concurrently
print("\n=== Bulk POST requests ===")
try:
    response = bulk_post(urls, data={"action": "update"})
    print(f"Status: {response.status}")
    print(f"Results count: {len(response.body['results'])}")
except Exception as e:
    print(f"Error: {e}")
