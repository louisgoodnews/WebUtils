"""
Header building examples for WebUtils.
"""

from webutils import HeaderBuilder

# Using HeaderBuilder with with_ methods
print("=== Using HeaderBuilder ===")
headers = (HeaderBuilder()
          .with_content_type("application/json")
          .with_accept("application/json")
          .with_authorization("Bearer token123")
          .with_user_agent("WebUtils/1.0")
          .with_cache_control("no-cache")
          .build())
print(f"Headers: {headers}")

# Available with_ methods:
# with_accept, with_accept_encoding, with_accept_language,
# with_authorization, with_cache_control, with_connection,
# with_content_encoding, with_content_length, with_content_type,
# with_cookie, with_host, with_if_modified_since, with_if_none_match,
# with_origin, with_referer, with_set_cookie, with_user_agent
