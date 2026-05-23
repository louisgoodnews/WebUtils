"""
Author: Louis Goodnews
Date: 2025-08-08
"""

from typing import Any, Dict, Optional, Self
from urllib.parse import urlencode, urlparse, urlunparse


class URL:
    """
    URL class that works analogous to pathlib.Path but for URLs.

    This class provides an object-oriented interface to URL manipulation,
    similar to how pathlib.Path works for filesystem paths.
    """

    def __init__(self, url: str) -> None:
        """
        Initialize the URL object.

        :param url: The URL string.
        :type url: str

        :return: None
        :rtype: None
        """
        self._parsed = urlparse(url)

    def __str__(self) -> str:
        """
        Return the URL as a string.

        :return: The URL string.
        :rtype: str
        """
        return self._parsed.geturl()

    def __repr__(self) -> str:
        """
        Return the string representation of the URL object.

        :return: The string representation.
        :rtype: str
        """
        return f"URL('{self._parsed.geturl()}')"

    def __truediv__(self, other: str) -> "URL":
        """
        Join a path segment to the URL using the / operator.

        :param other: The path segment to join.
        :type other: str

        :return: A new URL object with the joined path.
        :rtype: URL
        """
        return self.joinpath(other)

    @property
    def scheme(self) -> str:
        """
        Return the scheme of the URL (e.g., 'http', 'https').

        :return: The scheme.
        :rtype: str
        """
        return self._parsed.scheme

    @property
    def netloc(self) -> str:
        """
        Return the network location (e.g., 'example.com:8080').

        :return: The network location.
        :rtype: str
        """
        return self._parsed.netloc

    @property
    def hostname(self) -> str:
        """
        Return the hostname (e.g., 'example.com').

        :return: The hostname.
        :rtype: str
        """
        return self._parsed.hostname or ""

    @property
    def port(self) -> Optional[int]:
        """
        Return the port number.

        :return: The port number or None if not specified.
        :rtype: Optional[int]
        """
        return self._parsed.port

    @property
    def path(self) -> str:
        """
        Return the path component of the URL.

        :return: The path.
        :rtype: str
        """
        return self._parsed.path

    @property
    def query(self) -> str:
        """
        Return the query string.

        :return: The query string.
        :rtype: str
        """
        return self._parsed.query

    @property
    def fragment(self) -> str:
        """
        Return the fragment identifier.

        :return: The fragment.
        :rtype: str
        """
        return self._parsed.fragment

    @property
    def username(self) -> Optional[str]:
        """
        Return the username for authentication.

        :return: The username or None.
        :rtype: Optional[str]
        """
        return self._parsed.username

    @property
    def password(self) -> Optional[str]:
        """
        Return the password for authentication.

        :return: The password or None.
        :rtype: Optional[str]
        """
        return self._parsed.password

    def joinpath(self, *segments: str) -> "URL":
        """
        Join path segments to the URL.

        :param segments: Path segments to join.
        :type segments: str

        :return: A new URL object with the joined path.
        :rtype: URL
        """
        current_path = self._parsed.path.rstrip("/")
        new_path = "/".join([current_path] + list(segments))
        new_parsed = self._parsed._replace(path=new_path)
        return URL(urlunparse(new_parsed))

    def with_scheme(self, scheme: str) -> "URL":
        """
        Return a new URL with the scheme replaced.

        :param scheme: The new scheme.
        :type scheme: str

        :return: A new URL object.
        :rtype: URL
        """
        new_parsed = self._parsed._replace(scheme=scheme)
        return URL(urlunparse(new_parsed))

    def with_netloc(self, netloc: str) -> "URL":
        """
        Return a new URL with the netloc replaced.

        :param netloc: The new network location.
        :type netloc: str

        :return: A new URL object.
        :rtype: URL
        """
        new_parsed = self._parsed._replace(netloc=netloc)
        return URL(urlunparse(new_parsed))

    def with_path(self, path: str) -> "URL":
        """
        Return a new URL with the path replaced.

        :param path: The new path.
        :type path: str

        :return: A new URL object.
        :rtype: URL
        """
        new_parsed = self._parsed._replace(path=path)
        return URL(urlunparse(new_parsed))

    def with_query(self, **params: Any) -> "URL":
        """
        Return a new URL with query parameters.

        :param params: Query parameters.
        :type params: Dict[str, Any]

        :return: A new URL object.
        :rtype: URL
        """
        query_string = urlencode(params)
        new_parsed = self._parsed._replace(query=query_string)
        return URL(urlunparse(new_parsed))

    def with_fragment(self, fragment: str) -> "URL":
        """
        Return a new URL with the fragment replaced.

        :param fragment: The new fragment.
        :type fragment: str

        :return: A new URL object.
        :rtype: URL
        """
        new_parsed = self._parsed._replace(fragment=fragment)
        return URL(urlunparse(new_parsed))

    def add_param(self, key: str, value: Any) -> "URL":
        """
        Add a query parameter to the URL.

        :param key: The parameter key.
        :type key: str
        :param value: The parameter value.
        :type value: Any

        :return: A new URL object.
        :rtype: URL
        """
        from urllib.parse import parse_qs

        existing_params = parse_qs(self._parsed.query)
        existing_params[key] = [str(value)]
        query_string = urlencode(existing_params, doseq=True)
        new_parsed = self._parsed._replace(query=query_string)
        return URL(urlunparse(new_parsed))

    def remove_param(self, key: str) -> "URL":
        """
        Remove a query parameter from the URL.

        :param key: The parameter key to remove.
        :type key: str

        :return: A new URL object.
        :rtype: URL
        """
        from urllib.parse import parse_qs

        existing_params = parse_qs(self._parsed.query)
        existing_params.pop(key, None)
        query_string = urlencode(existing_params, doseq=True)
        new_parsed = self._parsed._replace(query=query_string)
        return URL(urlunparse(new_parsed))

    @property
    def name(self) -> str:
        """
        Return the final path component (like pathlib.Path.name).

        :return: The final path component.
        :rtype: str
        """
        path = self._parsed.path.rstrip("/")
        return path.split("/")[-1] if path else ""

    @property
    def stem(self) -> str:
        """
        Return the final path component without suffix (like pathlib.Path.stem).

        :return: The final path component without suffix.
        :rtype: str
        """
        name = self.name
        if "." in name:
            return name.rsplit(".", 1)[0]
        return name

    @property
    def suffix(self) -> str:
        """
        Return the file extension of the final path component (like pathlib.Path.suffix).

        :return: The file extension including the dot.
        :rtype: str
        """
        name = self.name
        if "." in name:
            return "." + name.rsplit(".", 1)[1]
        return ""

    @property
    def parent(self) -> "URL":
        """
        Return the parent URL (like pathlib.Path.parent).

        :return: The parent URL.
        :rtype: URL
        """
        path = self._parsed.path.rstrip("/")
        parent_path = "/".join(path.split("/")[:-1]) or "/"
        new_parsed = self._parsed._replace(path=parent_path)
        return URL(urlunparse(new_parsed))

    def absolute(self) -> "URL":
        """
        Return the absolute URL (always returns self as URLs are already absolute).

        :return: The URL object.
        :rtype: URL
        """
        return self

    def exists(self) -> bool:
        """
        Check if the URL exists (makes a HEAD request).

        :return: True if the URL exists, False otherwise.
        :rtype: bool
        """
        from .service import HTTPService

        try:
            response = HTTPService.head(str(self))
            return 200 <= response.status < 400
        except Exception:
            return False

    def as_dict(self) -> Dict[str, Optional[str]]:
        """
        Return the URL components as a dictionary.

        :return: Dictionary of URL components.
        :rtype: Dict[str, Optional[str]]
        """
        return {
            "scheme": self.scheme,
            "netloc": self.netloc,
            "path": self.path,
            "query": self.query,
            "fragment": self.fragment,
            "username": self.username,
            "password": self.password,
            "hostname": self.hostname,
            "port": str(self.port) if self.port is not None else None,
        }


class URLFactory:
    """
    URL Factory class.

    This class is used to create URL objects.
    """

    @classmethod
    def create_url(cls, url: str) -> URL:
        """
        Create a URL object.

        :param url: The URL string.
        :type url: str

        :return: The URL object.
        :rtype: URL
        """
        return URL(url)

    @classmethod
    def from_components(
        cls,
        scheme: str = "",
        netloc: str = "",
        path: str = "",
        params: str = "",
        query: str = "",
        fragment: str = "",
    ) -> URL:
        """
        Create a URL object from components.

        :param scheme: The scheme (e.g., 'http', 'https').
        :type scheme: str
        :param netloc: The network location.
        :type netloc: str
        :param path: The path.
        :type path: str
        :param params: The parameters (legacy, rarely used).
        :type params: str
        :param query: The query string.
        :type query: str
        :param fragment: The fragment.
        :type fragment: str

        :return: The URL object.
        :rtype: URL
        """
        url = urlunparse((scheme, netloc, path, params, query, fragment))
        return URL(url)


class URLBuilder:
    """
    URLBuilder class.

    This class is used to build URL objects using the builder pattern.
    """

    def __init__(
        self,
        url: str = "",
    ) -> None:
        """
        Initialize the URLBuilder object.

        :param url: The URL to build.
        :type url: str

        :return: None
        :rtype: None
        """

        # Initialize the configuration
        self._configuration: Dict[str, str] = {"url": url}

    def build(self) -> URL:
        """
        Build the URL object.

        :return: The URL object.
        :rtype: URL
        """
        return URLFactory.create_url(self._configuration["url"])

    def with_endpoint(
        self,
        value: str,
    ) -> Self:
        """
        Set the endpoint of the URL.

        :param value: The endpoint of the URL.
        :type value: str

        :return: The builder to the caller.
        :rtype: Self
        """

        # Set the endpoint
        self._configuration["url"] = f"{self._configuration['url']}/{value}"

        # Return the builder to the caller
        return self

    def with_endpoint_query(
        self,
        value: str,
        **kwargs: Any,
    ) -> Self:
        """
        Set the endpoint and query of the URL.

        :param value: The endpoint of the URL.
        :type value: str
        :param kwargs: The query of the URL.
        :type kwargs: Dict[str, Any]

        :return: The builder to the caller.
        :rtype: Self
        """

        # Set the endpoint and query
        query_string = urlencode(kwargs)
        self._configuration["url"] = (
            f"{self._configuration['url']}/{value}?{query_string}"
        )

        # Return the builder to the caller
        return self

    def with_fragment(
        self,
        value: str,
    ) -> Self:
        """
        Set the fragment of the URL.

        :param value: The fragment of the URL.
        :type value: str

        :return: The builder to the caller.
        :rtype: Self
        """

        # Set the fragment
        self._configuration["url"] = f"{self._configuration['url']}#{value}"

        # Return the builder to the caller
        return self

    def with_query(
        self,
        **kwargs: Any,
    ) -> Self:
        """
        Set the query of the URL.

        :param kwargs: The query of the URL.
        :type kwargs: Dict[str, Any]

        :return: The builder to the caller.
        :rtype: Self
        """

        # Set the query
        query_string = urlencode(kwargs)
        self._configuration["url"] = f"{self._configuration['url']}?{query_string}"

        # Return the builder to the caller
        return self

    def with_url(
        self,
        value: str,
    ) -> Self:
        """
        Set the base URL.

        :param value: The base URL.
        :type value: str

        :return: The builder to the caller.
        :rtype: Self
        """

        # Set the base URL
        self._configuration["url"] = value

        # Return the builder to the caller
        return self
