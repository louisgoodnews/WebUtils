"""
Author: Louis Goodnews
Date: 2025-08-08
"""

import base64
from typing import Dict, Final, Literal, Self


class Authorization:
    """
    Authorization class.

    This class is used to represent the authorization.
    """

    def __init__(
        self,
        password: str,
        username: str,
    ) -> None:
        """
        Initialize the Authorization object.

        :param password: The password of the authorization.
        :type password: str
        :param username: The username of the authorization.
        :type username: str

        :return: None
        :rtype: None
        """

        # Store the password of the authorization
        self._password: Final[str] = password

        # Store the username of the authorization
        self._username: Final[str] = username

    def __repr__(self) -> str:
        """
        Return the string representation of the Authorization object.

        :return: The string representation of the Authorization object.
        :rtype: str
        """

        # Return the string representation of the Authorization object
        return f"Authorization(password={'*'*len(self._password)}, username={self._username})"

    def __str__(self) -> str:
        """
        Return the string representation of the Authorization object.

        :return: The string representation of the Authorization object.
        :rtype: str
        """

        # Return the string representation of the Authorization object
        return self.__repr__()

    @property
    def password(self) -> str:
        """
        Return the password of the authorization.

        :return: The password of the authorization.
        :rtype: str
        """

        # Return the password of the authorization
        return self._password

    @property
    def username(self) -> str:
        """
        Return the username of the authorization.

        :return: The username of the authorization.
        :rtype: str
        """

        # Return the username of the authorization
        return self._username

    def basic(self) -> str:
        """
        Return the basic authorization.

        :return: The basic authorization.
        :rtype: str
        """

        # Return the basic authorization
        encoded = base64.b64encode(
            f"{self._username}:{self._password}".encode("utf-8")
        ).decode("utf-8")
        return f"Basic {encoded}"

    def bearer(self) -> str:
        """
        Return the bearer authorization.

        :return: The bearer authorization.
        :rtype: str
        """

        # Return the bearer authorization
        return f"Bearer {self._password}"

    def custom(
        self,
        scheme: str,
    ) -> str:
        """
        Return the custom authorization.

        :param scheme: The scheme of the authorization.
        :type scheme: str

        :return: The custom authorization.
        :rtype: str
        """

        # Return the custom authorization
        return f"{scheme} {self._password}"

    def digest(self) -> str:
        """
        Return the digest authorization.

        :return: The digest authorization.
        :rtype: str
        """

        # Return the digest authorization
        return f"Digest {self._password}"

    def header(
        self,
        scheme: Literal[
            "basic",
            "bearer",
            "custom",
            "digest",
            "oauth",
            "oauth2",
        ] = "basic",
    ) -> Dict[str, str]:
        """
        Return the header authorization.

        :param scheme: The scheme of the authorization.
        :type scheme: Literal["basic", "bearer", "custom", "digest", "oauth", "oauth2"]

        :return: The header authorization.
        :rtype: Dict[str, str]
        """

        # Return the header authorization
        return {"Authorization": getattr(self, scheme)()}

    def oauth(self) -> str:
        """
        Return the oauth authorization.

        :return: The oauth authorization.
        :rtype: str
        """

        # Return the oauth authorization
        return f"OAuth {self._password}"

    def oauth2(self) -> str:
        """
        Return the oauth2 authorization.

        :return: The oauth2 authorization.
        :rtype: str
        """

        # Return the oauth2 authorization
        return f"OAuth2 {self._password}"


class AuthorizationFactory:
    """
    Authorization Factory class.

    This class is used to create Authorization objects.
    """

    @classmethod
    def create_authorization(
        cls,
        password: str,
        username: str,
    ) -> Authorization:
        """
        Create an Authorization object.

        :param password: The password of the authorization.
        :type password: str
        :param username: The username of the authorization.
        :type username: str

        :return: The Authorization object.
        :rtype: Authorization
        """

        # Create and return the Authorization object
        return Authorization(
            password=password,
            username=username,
        )


class AuthorizationBuilder:
    """
    Authorization Builder class.

    This class is used to build Authorization objects.
    """

    def __init__(self) -> None:
        """
        Initialize the AuthorizationBuilder object.

        :return: None
        :rtype: None
        """

        # Initialize the configuration of the Authorization object
        self._configuration: Dict[str, str] = {}

    def build(self) -> Authorization:
        """
        Build the Authorization object.

        :return: The Authorization object.
        :rtype: Authorization

        :raises Exception: If the configuration is invalid.
        """
        try:
            # Return the Authorization object
            return AuthorizationFactory.create_authorization(
                password=self._configuration["password"],
                username=self._configuration["username"],
            )
        except Exception as e:
            # Raise the exception
            raise e

    def with_password(
        self,
        value: str,
    ) -> Self:
        """
        Set the password of the authorization.

        :param value: The password of the authorization.
        :type value: str

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the password of the authorization
        self._configuration["password"] = value

        # Return the builder to the caller
        return self

    def with_username(
        self,
        value: str,
    ) -> Self:
        """
        Set the username of the authorization.

        :param value: The username of the authorization.
        :type value: str

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the username of the authorization
        self._configuration["username"] = value

        # Return the builder to the caller
        return self
