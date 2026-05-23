"""
Author: Louis Goodnews
Date: 2025-08-08
"""

from typing import Dict, Self


class HeaderBuilder:
    """
    HeaderBuilder class.

    This class is used to build the header configuration.
    """

    def __init__(self) -> None:
        """
        Initialize the HeaderBuilder object.

        :return: None
        :rtype: None
        """

        self._configuration: Dict[str, str] = {}

    def add(
        self,
        key: str,
        value: str,
    ) -> Self:
        """
        Add a header to the configuration.

        :param key: The key of the header.
        :type key: str
        :param value: The value of the header.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: HeaderBuilder
        """

        # Add the header to the configuration
        self._configuration[key] = value

        # Return the HeaderBuilder object
        return self

    def build(self) -> Dict[str, str]:
        """
        Build the header configuration.

        :return: The header configuration.
        :rtype: Dict[str, str]
        """

        # Return the header configuration
        return self._configuration

    def with_accept(
        self,
        value: str,
    ) -> Self:
        """
        Set the Accept header.

        :param value: The Accept header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Accept header
        self._configuration["Accept"] = value

        # Return the HeaderBuilder object
        return self

    def with_accept_encoding(
        self,
        value: str,
    ) -> Self:
        """
        Set the Accept-Encoding header.

        :param value: The Accept-Encoding header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Accept-Encoding header
        self._configuration["Accept-Encoding"] = value

        # Return the HeaderBuilder object
        return self

    def with_accept_language(
        self,
        value: str,
    ) -> Self:
        """
        Set the Accept-Language header.

        :param value: The Accept-Language header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Accept-Language header
        self._configuration["Accept-Language"] = value

        # Return the HeaderBuilder object
        return self

    def with_authorization(
        self,
        value: str,
    ) -> Self:
        """
        Set the Authorization header.

        :param value: The Authorization header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Authorization header
        self._configuration["Authorization"] = value

        # Return the HeaderBuilder object
        return self

    def with_cache_control(
        self,
        value: str,
    ) -> Self:
        """
        Set the Cache-Control header.

        :param value: The Cache-Control header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Cache-Control header
        self._configuration["Cache-Control"] = value

        # Return the HeaderBuilder object
        return self

    def with_connection(
        self,
        value: str,
    ) -> Self:
        """
        Set the Connection header.

        :param value: The Connection header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Connection header
        self._configuration["Connection"] = value

        # Return the HeaderBuilder object
        return self

    def with_content_encoding(
        self,
        value: str,
    ) -> Self:
        """
        Set the Content-Encoding header.

        :param value: The Content-Encoding header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Content-Encoding header
        self._configuration["Content-Encoding"] = value

        # Return the HeaderBuilder object
        return self

    def with_content_length(
        self,
        value: str,
    ) -> Self:
        """
        Set the Content-Length header.

        :param value: The Content-Length header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Content-Length header
        self._configuration["Content-Length"] = value

        # Return the HeaderBuilder object
        return self

    def with_content_type(
        self,
        value: str,
    ) -> Self:
        """
        Set the Content-Type header.

        :param value: The Content-Type header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Content-Type header
        self._configuration["Content-Type"] = value

        # Return the HeaderBuilder object
        return self

    def with_cookie(
        self,
        value: str,
    ) -> Self:
        """
        Set the Cookie header.

        :param value: The Cookie header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Cookie header
        self._configuration["Cookie"] = value

        # Return the HeaderBuilder object
        return self

    def with_host(
        self,
        value: str,
    ) -> Self:
        """
        Set the Host header.

        :param value: The Host header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Host header
        self._configuration["Host"] = value

        # Return the HeaderBuilder object
        return self

    def with_if_modified_since(
        self,
        value: str,
    ) -> Self:
        """
        Set the If-Modified-Since header.

        :param value: The If-Modified-Since header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the If-Modified-Since header
        self._configuration["If-Modified-Since"] = value

        # Return the HeaderBuilder object
        return self

    def with_if_none_match(
        self,
        value: str,
    ) -> Self:
        """
        Set the If-None-Match header.

        :param value: The If-None-Match header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the If-None-Match header
        self._configuration["If-None-Match"] = value

        # Return the HeaderBuilder object
        return self

    def with_origin(
        self,
        value: str,
    ) -> Self:
        """
        Set the Origin header.

        :param value: The Origin header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Origin header
        self._configuration["Origin"] = value

        # Return the HeaderBuilder object
        return self

    def with_referer(
        self,
        value: str,
    ) -> Self:
        """
        Set the Referer header.

        :param value: The Referer header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Referer header
        self._configuration["Referer"] = value

        # Return the HeaderBuilder object
        return self

    def with_set_cookie(
        self,
        value: str,
    ) -> Self:
        """
        Set the Set-Cookie header.

        :param value: The Set-Cookie header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the Set-Cookie header
        self._configuration["Set-Cookie"] = value

        # Return the HeaderBuilder object
        return self

    def with_user_agent(
        self,
        value: str,
    ) -> Self:
        """
        Set the User-Agent header.

        :param value: The User-Agent header value.
        :type value: str

        :return: The HeaderBuilder object.
        :rtype: Self
        """

        # Set the User-Agent header
        self._configuration["User-Agent"] = value

        # Return the HeaderBuilder object
        return self
