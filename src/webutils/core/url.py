"""
Author: Louis Goodnews
Date: 2025-08-08
"""

from typing import Any, Dict, List, Optional, Self, Union
from urllib.parse import urlencode, parse_qs, urlparse, urlunparse


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


class URLQuery:
    """
    URLQuery class for managing URL query parameters.

    This class provides an object-oriented interface to query parameter manipulation,
    with support for multiple values per parameter and type-safe operations.
    """

    def __init__(
        self,
        query: Optional[str] = None,
        params: Optional[Dict[str, Union[str, List[str]]]] = None,
    ) -> None:
        """
        Initialize the URLQuery object.

        :param query: The query string (e.g., "key1=value1&key2=value2").
        :type query: Optional[str]
        :param params: Dictionary of parameters (can have list values for multiple values).
        :type params: Optional[Dict[str, Union[str, List[str]]]]

        :return: None
        :rtype: None
        """
        if params:
            self._params: Dict[str, List[str]] = {
                k: [v] if isinstance(v, str) else v for k, v in params.items()
            }
        elif query:
            self._params = parse_qs(query)
        else:
            self._params = {}

    def __str__(self) -> str:
        """
        Return the query string.

        :return: The query string.
        :rtype: str
        """
        return urlencode(self._params, doseq=True)

    def __repr__(self) -> str:
        """
        Return the string representation of the URLQuery object.

        :return: The string representation.
        :rtype: str
        """
        return f"URLQuery('{str(self)}')"

    def __getitem__(self, key: str) -> List[str]:
        """
        Get the value(s) for a parameter key.

        :param key: The parameter key.
        :type key: str

        :return: The value(s) for the key.
        :rtype: List[str]
        """
        return self._params.get(key, [])

    def __setitem__(self, key: str, value: Union[str, List[str]]) -> None:
        """
        Set the value(s) for a parameter key.

        :param key: The parameter key.
        :type key: str
        :param value: The value(s) for the key.
        :type value: Union[str, List[str]]

        :return: None
        :rtype: None
        """
        self._params[key] = [value] if isinstance(value, str) else value

    def __delitem__(self, key: str) -> None:
        """
        Delete a parameter key.

        :param key: The parameter key.
        :type key: str

        :return: None
        :rtype: None
        """
        del self._params[key]

    def __contains__(self, key: str) -> bool:
        """
        Check if a parameter key exists.

        :param key: The parameter key.
        :type key: str

        :return: True if the key exists, False otherwise.
        :rtype: bool
        """
        return key in self._params

    def __len__(self) -> int:
        """
        Return the number of parameters.

        :return: The number of parameters.
        :rtype: int
        """
        return len(self._params)

    def __iter__(self):
        """
        Iterate over parameter keys.

        :return: Iterator over parameter keys.
        :rtype: Iterator[str]
        """
        return iter(self._params)

    @property
    def params(self) -> Dict[str, List[str]]:
        """
        Get the parameters dictionary.

        :return: The parameters dictionary.
        :rtype: Dict[str, List[str]]
        """
        return self._params.copy()

    def add(self, key: str, value: Union[str, List[str]]) -> Self:
        """
        Add a parameter (or append to existing).

        :param key: The parameter key.
        :type key: str
        :param value: The value(s) for the key.
        :type value: Union[str, List[str]]

        :return: Self for method chaining.
        :rtype: Self
        """
        if key in self._params:
            if isinstance(value, str):
                self._params[key].append(value)
            else:
                self._params[key].extend(value)
        else:
            self._params[key] = [value] if isinstance(value, str) else value
        return self

    def set(self, key: str, value: Union[str, List[str]]) -> Self:
        """
        Set a parameter (overwrites existing).

        :param key: The parameter key.
        :type key: str
        :param value: The value(s) for the key.
        :type value: Union[str, List[str]]

        :return: Self for method chaining.
        :rtype: Self
        """
        self._params[key] = [value] if isinstance(value, str) else value
        return self

    def remove(self, key: str) -> Self:
        """
        Remove a parameter.

        :param key: The parameter key.
        :type key: str

        :return: Self for method chaining.
        :rtype: Self
        """
        if key in self._params:
            del self._params[key]
        return self

    def get(self, key: str, default: Optional[List[str]] = None) -> List[str]:
        """
        Get the value(s) for a parameter key with default.

        :param key: The parameter key.
        :type key: str
        :param default: The default value if key doesn't exist.
        :type default: Optional[List[str]]

        :return: The value(s) for the key or default.
        :rtype: List[str]
        """
        return self._params.get(key, default or [])

    def get_first(self, key: str, default: Optional[str] = None) -> str:
        """
        Get the first value for a parameter key with default.

        :param key: The parameter key.
        :type key: str
        :param default: The default value if key doesn't exist.
        :type default: Optional[str]

        :return: The first value for the key or default.
        :rtype: str
        """
        values = self._params.get(key, [])
        return values[0] if values else default or ""

    def has(self, key: str) -> bool:
        """
        Check if a parameter key exists.

        :param key: The parameter key.
        :type key: str

        :return: True if the key exists, False otherwise.
        :rtype: bool
        """
        return key in self._params

    def clear(self) -> Self:
        """
        Clear all parameters.

        :return: Self for method chaining.
        :rtype: Self
        """
        self._params.clear()
        return self

    def to_dict(self) -> Dict[str, Union[str, List[str]]]:
        """
        Convert to dictionary (single values as strings, multiple as lists).

        :return: Dictionary representation.
        :rtype: Dict[str, Union[str, List[str]]]
        """
        return {k: v[0] if len(v) == 1 else v for k, v in self._params.items()}

    def copy(self) -> "URLQuery":
        """
        Create a copy of the URLQuery object.

        :return: A copy of the URLQuery object.
        :rtype: URLQuery
        """
        return URLQuery(params=self._params.copy())


class URLQueryFactory:
    """
    URLQuery Factory class.

    This class provides factory methods to create URLQuery objects.
    """

    @classmethod
    def create_query(cls, query: Optional[str] = None) -> URLQuery:
        """
        Create a URLQuery object from a query string.

        :param query: The query string.
        :type query: Optional[str]

        :return: The URLQuery object.
        :rtype: URLQuery
        """
        return URLQuery(query=query)

    @classmethod
    def from_params(cls, params: Dict[str, Union[str, List[str]]]) -> URLQuery:
        """
        Create a URLQuery object from a parameters dictionary.

        :param params: The parameters dictionary.
        :type params: Dict[str, Union[str, List[str]]]

        :return: The URLQuery object.
        :rtype: URLQuery
        """
        return URLQuery(params=params)

    @classmethod
    def from_url(cls, url: str) -> URLQuery:
        """
        Create a URLQuery object from a URL string.

        :param url: The URL string.
        :type url: str

        :return: The URLQuery object.
        :rtype: URLQuery
        """
        parsed = urlparse(url)
        return URLQuery(query=parsed.query)


class URLQueryBuilder:
    """
    URLQuery Builder class.

    This class provides a fluent builder interface for constructing URLQuery objects.
    """

    def __init__(self, query: Optional[str] = None) -> None:
        """
        Initialize the URLQueryBuilder.

        :param query: The initial query string.
        :type query: Optional[str]

        :return: None
        :rtype: None
        """
        self._query: URLQuery = URLQuery(query=query)

    def add_param(self, key: str, value: Union[str, List[str]]) -> Self:
        """
        Add a parameter (or append to existing).

        :param key: The parameter key.
        :type key: str
        :param value: The value(s) for the key.
        :type value: Union[str, List[str]]

        :return: Self for method chaining.
        :rtype: Self
        """
        self._query.add(key, value)
        return self

    def set_param(self, key: str, value: Union[str, List[str]]) -> Self:
        """
        Set a parameter (overwrites existing).

        :param key: The parameter key.
        :type key: str
        :param value: The value(s) for the key.
        :type value: Union[str, List[str]]

        :return: Self for method chaining.
        :rtype: Self
        """
        self._query.set(key, value)
        return self

    def remove_param(self, key: str) -> Self:
        """
        Remove a parameter.

        :param key: The parameter key.
        :type key: str

        :return: Self for method chaining.
        :rtype: Self
        """
        self._query.remove(key)
        return self

    def clear_params(self) -> Self:
        """
        Clear all parameters.

        :return: Self for method chaining.
        :rtype: Self
        """
        self._query.clear()
        return self

    def with_params(self, params: Dict[str, Union[str, List[str]]]) -> Self:
        """
        Set multiple parameters at once.

        :param params: The parameters dictionary.
        :type params: Dict[str, Union[str, List[str]]]

        :return: Self for method chaining.
        :rtype: Self
        """
        self._query.clear()
        for key, value in params.items():
            self._query.set(key, value)
        return self

    def build(self) -> URLQuery:
        """
        Build and return the URLQuery object.

        :return: The URLQuery object.
        :rtype: URLQuery
        """
        return self._query


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
        self._query_builder: Optional[URLQueryBuilder] = None

    def build(self) -> URL:
        """
        Build the URL object.

        :return: The URL object.
        :rtype: URL
        """
        url = self._configuration["url"]

        # Apply query parameters if URLQueryBuilder is set
        if self._query_builder:
            query = self._query_builder.build()
            if str(query):
                separator = "&" if "?" in url else "?"
                url = f"{url}{separator}{str(query)}"

        return URLFactory.create_url(url)

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

        # Use URLQueryBuilder for query parameter management
        if self._query_builder is None:
            self._query_builder = URLQueryBuilder()

        for key, value in kwargs.items():
            self._query_builder.set_param(key, str(value))

        return self

    def with_query_builder(
        self,
        query_builder: URLQueryBuilder,
    ) -> Self:
        """
        Set the query using a URLQueryBuilder.

        :param query_builder: The URLQueryBuilder object.
        :type query_builder: URLQueryBuilder

        :return: The builder to the caller.
        :rtype: Self
        """
        self._query_builder = query_builder
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
