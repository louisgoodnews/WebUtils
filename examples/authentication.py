"""
Authentication examples for WebUtils.
"""

from webutils import Authorization, AuthorizationBuilder, AuthorizationFactory

# Using Authorization class directly
print("=== Using Authorization class ===")
auth = Authorization(username="user", password="pass")
print(f"Basic auth: {auth.basic()}")
print(f"Bearer auth: {auth.bearer()}")
print(f"OAuth auth: {auth.oauth()}")
print(f"Header (basic): {auth.header('basic')}")

# Using AuthorizationBuilder
print("\n=== Using AuthorizationBuilder ===")
auth = (AuthorizationBuilder()
        .with_username("user")
        .with_password("pass")
        .build())
print(f"Basic auth: {auth.basic()}")

# Using AuthorizationFactory
print("\n=== Using AuthorizationFactory ===")
auth = AuthorizationFactory.create_authorization("user", "pass")
print(f"Basic auth: {auth.basic()}")
