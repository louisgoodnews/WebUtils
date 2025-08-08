"""
Author: Louis Goodnews
Date: 2025-08-08
"""

import aiohttp
import asyncio
import base64

from enum import Enum
from datetime import datetime
from typing import Any, Dict, Final, List, Literal, Optional, Self, Union


__all__: Final[List[str]] = [
    "Authorization",
    "HeaderBuilder",
    "HTTPMethod",
    "HTTPResponse",
    "HTTPResponseFactory",
    "HTTPResponseBuilder",
    "HTTPService",
    "URLBuilder",
]


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
        return f"Basic {base64.b64encode(f'{self._username}:{self._password}'.encode('utf-8')).decode('utf-8')}"

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


class HTTPMethod(Enum):
    """
    HTTP Method enum.

    This class is used to represent the HTTP method.

    :cvar GET: GET method.
    :cvar POST: POST method.
    :cvar PUT: PUT method.
    :cvar DELETE: DELETE method.
    :cvar PATCH: PATCH method.
    :cvar HEAD: HEAD method.
    :cvar OPTIONS: OPTIONS method.
    :cvar TRACE: TRACE method.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"

    def __str__(self) -> str:
        """
        Return the value of the enum member.

        :return: The value of the enum member.
        :rtype: str
        """

        # Return the value of the enum member
        return self.value


class HTTPResponse:
    """
    HTTP Response class.

    This class is used to represent the HTTP response.

    Attributes:
        body (Dict[str, Any]): The body of the response.
        duration (float): The duration of the response.
        end (datetime): The end time of the response.
        headers (Dict[str, Any]): The headers of the response.
        message (str): The message of the response.
        method (HTTPMethod): The method of the response.
        start (datetime): The start time of the response.
        status (int): The status of the response.
        type (str): The type of the response.
        url (str): The URL of the response.
    """

    def __init__(
        self,
        end: datetime,
        headers: Dict[str, Any],
        message: str,
        method: HTTPMethod,
        start: datetime,
        status: int,
        type: str,
        url: str,
        body: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the HTTPResponse object.

        :param body: The body of the response.
        :type body: Optional[Dict[str, Any]]
        :param end: The end time of the response.
        :type end: datetime
        :param headers: The headers of the response.
        :type headers: Dict[str, Any]
        :param message: The message of the response.
        :type message: str
        :param method: The method of the response.
        :type method: HTTPMethod
        :param start: The start time of the response.
        :type start: datetime
        :param status: The status of the response.
        :type status: int
        :param type: The type of the response.
        :type type: str
        :param url: The URL of the response.
        :type url: str

        :return: None
        :rtype: None
        """

        # Store the body of the response
        self._body: Final[Dict[str, Any]] = body or {}

        # Store the end time of the response
        self._end: Final[datetime] = end

        # Store the headers of the response
        self._headers: Final[Dict[str, Any]] = headers

        # Store the message of the response
        self._message: Final[str] = message

        # Store the method of the response
        self._method: Final[HTTPMethod] = method

        # Store the start time of the response
        self._start: Final[datetime] = start

        # Store the status of the response
        self._status: Final[int] = status

        # Store the type of the response
        self._type: Final[str] = type

        # Store the URL of the response
        self._url: Final[str] = url

        # Store the duration of the response
        self._duration: Final[float] = (end - start).total_seconds()

    def __getitem__(
        self,
        key: str,
    ) -> Optional[Any]:
        """
        Return the value of the key in the body of the response.

        :param key: The key to look for in the body of the response.
        :type key: str

        :return: The value of the key in the body of the response.
        :rtype: Optional[Any]
        """

        # Return the value of the key in the body of the response
        return self._body.get(
            key,
            None,
        )

    def __repr__(self) -> str:
        """
        Return the string representation of the HTTPResponse object.

        :return: The string representation of the HTTPResponse object.
        :rtype: str
        """

        # Return the string representation of the HTTPResponse object
        return f"HTTPResponse(body={self._body}, duration={self._duration}, end={self._end}, headers={self._headers}, message={self._message}, method={self._method}, start={self._start}, status={self._status}, type={self._type}, url={self._url})"

    def __str__(self) -> str:
        """
        Return the string representation of the HTTPResponse object.

        :return: The string representation of the HTTPResponse object.
        :rtype: str
        """

        # Return the string representation of the HTTPResponse object
        return self.__repr__()

    @property
    def body(self) -> Dict[str, Any]:
        """
        Return the body of the response.

        :return: The body of the response.
        :rtype: Dict[str, Any]
        """

        # Return the body of the response
        return self._body

    @property
    def duration(self) -> float:
        """
        Return the duration of the response.

        :return: The duration of the response.
        :rtype: float
        """

        # Return the duration of the response
        return self._duration

    @property
    def end(self) -> datetime:
        """
        Return the end time of the response.

        :return: The end time of the response.
        :rtype: datetime
        """

        # Return the end time of the response
        return self._end

    @property
    def headers(self) -> Dict[str, Any]:
        """
        Return the headers of the response.

        :return: The headers of the response.
        :rtype: Dict[str, Any]
        """

        # Return the headers of the response
        return self._headers

    @property
    def message(self) -> str:
        """
        Return the message of the response.

        :return: The message of the response.
        :rtype: str
        """

        # Return the message of the response
        return self._message

    @property
    def method(self) -> HTTPMethod:
        """
        Return the method of the response.

        :return: The method of the response.
        :rtype: HTTPMethod
        """

        # Return the method of the response
        return self._method

    @property
    def start(self) -> datetime:
        """
        Return the start time of the response.

        :return: The start time of the response.
        :rtype: datetime
        """

        # Return the start time of the response
        return self._start

    @property
    def status(self) -> int:
        """
        Return the status of the response.

        :return: The status of the response.
        :rtype: int
        """

        # Return the status of the response
        return self._status

    @property
    def type(self) -> str:
        """
        Return the type of the response.

        :return: The type of the response.
        :rtype: str
        """

        # Return the type of the response
        return self._type

    @property
    def url(self) -> str:
        """
        Return the URL of the response.

        :return: The URL of the response.
        :rtype: str
        """

        # Return the URL of the response
        return self._url

    def dict(self) -> Dict[str, Any]:
        """
        Return the response as a dictionary.

        :return: The response as a dictionary.
        :rtype: Dict[str, Any]
        """

        # Return the response as a dictionary
        return {
            "body": self._body,
            "duration": self._duration,
            "end": self._end.strftime("%Y-%m-%d %H:%M:%S"),
            "headers": self._headers,
            "message": self._message,
            "method": self._method.value,
            "start": self._start.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self._status,
            "type": self._type,
            "url": self._url,
        }

    def empty(self) -> bool:
        """
        Return True if the response was empty, False otherwise.

        :return: True if the response was empty, False otherwise.
        :rtype: bool
        """

        # Return True if the response was empty, False otherwise
        return self._status == 204

    def success(self) -> bool:
        """
        Return True if the response was successful, False otherwise.

        :return: True if the response was successful, False otherwise.
        :rtype: bool
        """

        # Return True if the response was successful, False otherwise
        return self._status >= 200 and self._status < 300


class HTTPResponseFactory:
    """
    HTTP Response Factory class.

    This class is used to create HTTPResponse objects.
    """

    @classmethod
    def create_response(
        cls,
        end: datetime,
        headers: Dict[str, Any],
        message: str,
        method: HTTPMethod,
        start: datetime,
        status: int,
        type: str,
        url: str,
        body: Optional[Dict[str, Any]] = None,
    ) -> HTTPResponse:
        """
        Create an HTTPResponse object.

        :param end: The end time of the response.
        :type end: datetime
        :param headers: The headers of the response.
        :type headers: Dict[str, Any]
        :param message: The message of the response.
        :type message: str
        :param method: The method of the response.
        :type method: HTTPMethod
        :param start: The start time of the response.
        :type start: datetime
        :param status: The status of the response.
        :type status: int
        :param type: The type of the response.
        :type type: str
        :param url: The URL of the response.
        :type url: str
        :param body: The body of the response.
        :type body: Optional[Dict[str, Any]]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        # Create and return the HTTPResponse object
        return HTTPResponse(
            end=end,
            headers=headers,
            message=message,
            method=method,
            start=start,
            status=status,
            type=type,
            url=url,
            body=body,
        )


class HTTPResponseBuilder:
    """
    HTTP Response Builder class.

    This class is used to build HTTPResponse objects.
    """

    def __init__(self) -> None:
        """
        Initialize the HTTPResponseBuilder object.

        :return: None
        :rtype: None
        """

        # Initialize the configuration of the HTTPResponse object
        self._configuration: Dict[str, Any] = {}

    def build(self) -> HTTPResponse:
        """
        Build the HTTPResponse object.

        :return: The HTTPResponse object.
        :rtype: HTTPResponse

        :raises Exception: If the configuration is invalid.
        """
        try:
            # Return the HTTPResponse object
            return HTTPResponseFactory.create_response(
                end=self._configuration["end"],
                headers=self._configuration["headers"],
                message=self._configuration["message"],
                method=self._configuration["method"],
                start=self._configuration["start"],
                status=self._configuration["status"],
                type=self._configuration["type"],
                url=self._configuration["url"],
                body=self._configuration.get("body", {}),
            )
        except Exception as e:
            # Raise the exception
            raise e

    def with_body(
        self,
        value: Any,
    ) -> Self:
        """
        Set the body of the response.

        :param value: The body of the response.
        :type value: Any

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the body of the response
        self._configuration["body"] = (
            value if isinstance(value, dict) else {"body": value}
        )

        # Return the builder to the caller
        return self

    def with_end(
        self,
        value: datetime,
    ) -> Self:
        """
        Set the end time of the response.

        :param value: The end time of the response.
        :type value: datetime

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the end time of the response
        self._configuration["end"] = value

        # Return the buildHTTPServiceer to the caller
        return self

    def with_headers(
        self,
        value: Dict[str, Any],
    ) -> Self:
        """
        Set the headers of the response.

        :param value: The headers of the response.
        :type value: Dict[str, Any]

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the headers of the response
        self._configuration["headers"] = value

        # Return the builder to the caller
        return self

    def with_message(
        self,
        value: str,
    ) -> Self:
        """
        Set the message of the response.

        :param value: The message of the response.
        :type value: str

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the message of the response
        self._configuration["message"] = value

        # Return the builder to the caller
        return self

    def with_method(
        self,
        value: HTTPMethod,
    ) -> Self:
        """
        Set the method of the response.

        :param value: The method of the response.
        :type value: HTTPMethod

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the method of the response
        self._configuration["method"] = value

        # Return the builder to the caller
        return self

    def with_start(
        self,
        value: datetime,
    ) -> Self:
        """
        Set the start time of the response.

        :param value: The start time of the response.
        :type value: datetime

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the start time of the response
        self._configuration["start"] = value

        # Return the builder to the caller
        return self

    def with_status(
        self,
        value: int,
    ) -> Self:
        """
        Set the status of the response.

        :param value: The status of the response.
        :type value: int

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the status of the response
        self._configuration["status"] = value

        # Return the builder to the caller
        return self

    def with_type(
        self,
        value: str,
    ) -> Self:
        """
        Set the type of the response.

        :param value: The type of the response.
        :type value: str

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the type of the response
        self._configuration["type"] = value

        # Return the builder to the caller
        return self

    def with_url(
        self,
        value: str,
    ) -> Self:
        """
        Set the URL of the response.

        :param value: The URL of the response.
        :type value: str

        :return: The builder to the caller.
        :rtype: Self
        """

        # Store the URL of the response
        self._configuration["url"] = value

        # Return the builder to the caller
        return self


class HTTPService:
    """
    A service class to make HTTP requests to the specified URL.
    """

    @classmethod
    async def _handle_content_type(
        cls,
        content_type: str,
        response: aiohttp.ClientResponse,
    ) -> Union[
        bytes,
        Dict[str, Any],
        str,
    ]:
        """
        Handle the content type of the response.

        :param content_type: The content type of the response.
        :type content_type: str
        :param response: The response object.
        :type response: aiohttp.ClientResponse

        :return: The content of the response.
        :rtype: Union[bytes, Dict[str, Any], str]
        """

        if content_type == "application/json":
            return await response.json()
        elif content_type == "application/xml":
            return await response.text()
        elif content_type == "application/octet-stream":
            return await response.read()
        elif content_type.startswith("image/"):
            return await response.read()
        else:
            return await response.text()

    @classmethod
    def get(
        cls,
        url: str,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make a GET request to the specified URL.

        :param url: The URL to make the GET request to.
        :type url: str
        :param kwargs: Additional keyword arguments to pass to the GET request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __get__(
            url: str,
            **kwargs,
        ) -> HTTPResponse:
            """
            Make a GET request to the specified URL.

            :param url: The URL to make the GET request to.
            :type url: str
            :param kwargs: Additional keyword arguments to pass to the GET request.
            :type kwargs: Dict[str, Any]

            :return: The HTTPResponse object.
            :rtype: HTTPResponse
            """

            # Initialize the builder
            builder: HTTPResponseBuilder = HTTPResponseBuilder()

            # Set the method of the response
            builder.with_method(value=HTTPMethod.GET)

            # Set the URL of the response
            builder.with_url(value=url)

            # Set the headers of the response
            builder.with_headers(value={})

            # Set the start time of the response
            builder.with_start(value=datetime.now())

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    **kwargs,
                ) as response:
                    # Raise an exception if the response is not successful
                    response.raise_for_status()

                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the message of the response
                    builder.with_message(value=response.reason)

                    # Set the type of the response
                    builder.with_type(value=response.content_type)

                    builder.with_body(
                        await cls._handle_content_type(
                            content_type=response.content_type,
                            response=response,
                        )
                    )

                    # Set the end time of the response
                    builder.with_end(value=datetime.now())

            # Return the HTTPResponse object
            return builder.build()

        # Return the HTTPResponse object
        return asyncio.run(
            __get__(
                url=url,
                **kwargs,
            )
        )

    @classmethod
    def post(
        cls,
        url: str,
        data: Dict[str, Any] = {},
        headers: Dict[str, Any] = {},
        **kwargs,
    ) -> HTTPResponse:
        """
        Make a POST request to the specified URL.

        :param url: The URL to make the POST request to.
        :type url: str
        :param data: The data to send with the POST request.
        :type data: Dict[str, Any]
        :param headers: The headers to send with the POST request.
        :type headers: Dict[str, Any]
        :param kwargs: Additional keyword arguments to pass to the POST request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __post__(
            url: str,
            data: Dict[str, Any] = {},
            headers: Dict[str, Any] = {},
            **kwargs,
        ) -> HTTPResponse:
            """
            Make a POST request to the specified URL.

            :param url: The URL to make the POST request to.
            :type url: str
            :param data: The data to send with the POST request.
            :type data: Dict[str, Any]
            :param headers: The headers to send with the POST request.
            :type headers: Dict[str, Any]
            :param kwargs: Additional keyword arguments to pass to the POST request.
            :type kwargs: Dict[str, Any]

            :return: The HTTPResponse object.
            :rtype: HTTPResponse
            """

            # Initialize the builder
            builder: HTTPResponseBuilder = HTTPResponseBuilder()

            # Set the method of the response
            builder.with_method(value=HTTPMethod.POST)

            # Set the URL of the response
            builder.with_url(value=url)

            # Set the headers of the response
            builder.with_headers(value=headers)

            # Set the start time of the response
            builder.with_start(value=datetime.now())

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    data=data,
                    **kwargs,
                ) as response:
                    # Raise an exception if the response is not successful
                    response.raise_for_status()

                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=str.JSON)

                    # Set the message of the response
                    builder.with_message(value=response.reason)

                    builder.with_body(
                        await cls._handle_content_type(
                            content_type=response.content_type,
                            response=response,
                        )
                    )

                    # Set the end time of the response
                    builder.with_end(value=datetime.now())

            # Return the HTTPResponse object
            return builder.build()

        # Return the HTTPResponse object
        return asyncio.run(
            __post__(
                data=data,
                headers=headers,
                url=url,
                **kwargs,
            )
        )

    @classmethod
    def put(
        cls,
        url: str,
        data: Dict[str, Any] = {},
        headers: Dict[str, Any] = {},
        **kwargs,
    ) -> HTTPResponse:
        """
        Make a PUT request to the specified URL.

        :param url: The URL to make the PUT request to.
        :type url: str
        :param data: The data to send with the PUT request.
        :type data: Dict[str, Any]
        :param headers: The headers to send with the PUT request.
        :type headers: Dict[str, Any]
        :param kwargs: Additional keyword arguments to pass to the PUT request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __put__(
            url: str,
            data: Dict[str, Any] = {},
            headers: Dict[str, Any] = {},
            **kwargs,
        ) -> HTTPResponse:
            """
            Make a PUT request to the specified URL.

            :param url: The URL to make the PUT request to.
            :type url: str
            :param data: The data to send with the PUT request.
            :type data: Dict[str, Any]
            :param headers: The headers to send with the PUT request.
            :type headers: Dict[str, Any]
            :param kwargs: Additional keyword arguments to pass to the PUT request.
            :type kwargs: Dict[str, Any]

            :return: The HTTPResponse object.
            :rtype: HTTPResponse
            """

            # Initialize the builder
            builder: HTTPResponseBuilder = HTTPResponseBuilder()

            # Set the method of the response
            builder.with_method(value=HTTPMethod.PUT)

            # Set the URL of the response
            builder.with_url(value=url)

            # Set the headers of the response
            builder.with_headers(value=headers)

            # Set the start time of the response
            builder.with_start(value=datetime.now())

            async with aiohttp.ClientSession() as session:
                async with session.put(
                    url,
                    headers=headers,
                    data=data,
                    **kwargs,
                ) as response:
                    # Raise an exception if the response is not successful
                    response.raise_for_status()

                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=str.JSON)

                    # Set the message of the response
                    builder.with_message(value=response.reason)

                    builder.with_body(
                        await cls._handle_content_type(
                            content_type=response.content_type,
                            response=response,
                        )
                    )

                    # Set the end time of the response
                    builder.with_end(value=datetime.now())

            # Return the HTTPResponse object
            return builder.build()

        # Return the HTTPResponse object
        return asyncio.run(
            __put__(
                data=data,
                headers=headers,
                url=url,
                **kwargs,
            )
        )

    @classmethod
    def delete(
        cls,
        url: str,
        data: Dict[str, Any] = {},
        headers: Dict[str, Any] = {},
        **kwargs,
    ) -> HTTPResponse:
        """
        Make a DELETE request to the specified URL.

        :param url: The URL to make the DELETE request to.
        :type url: str
        :param data: The data to send with the DELETE request.
        :type data: Dict[str, Any]
        :param headers: The headers to send with the DELETE request.
        :type headers: Dict[str, Any]
        :param kwargs: Additional keyword arguments to pass to the DELETE request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __delete__(
            url: str,
            data: Dict[str, Any] = {},
            headers: Dict[str, Any] = {},
            **kwargs,
        ) -> HTTPResponse:
            """
            Make a DELETE request to the specified URL.

            :param url: The URL to make the DELETE request to.
            :type url: str
            :param data: The data to send with the DELETE request.
            :type data: Dict[str, Any]
            :param headers: The headers to send with the DELETE request.
            :type headers: Dict[str, Any]
            :param kwargs: Additional keyword arguments to pass to the DELETE request.
            :type kwargs: Dict[str, Any]

            :return: The HTTPResponse object.
            :rtype: HTTPResponse
            """

            # Initialize the builder
            builder: HTTPResponseBuilder = HTTPResponseBuilder()

            # Set the method of the response
            builder.with_method(value=HTTPMethod.DELETE)

            # Set the URL of the response
            builder.with_url(value=url)

            # Set the headers of the response
            builder.with_headers(value=headers)

            # Set the start time of the response
            builder.with_start(value=datetime.now())

            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    url,
                    headers=headers,
                    data=data,
                    **kwargs,
                ) as response:
                    # Raise an exception if the response is not successful
                    response.raise_for_status()

                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=str.JSON)

                    # Set the message of the response
                    builder.with_message(value=response.reason)

                    builder.with_body(
                        await cls._handle_content_type(
                            content_type=response.content_type,
                            response=response,
                        )
                    )

                    # Set the end time of the response
                    builder.with_end(value=datetime.now())

            # Return the HTTPResponse object
            return builder.build()

        # Return the HTTPResponse object
        return asyncio.run(
            __delete__(
                data=data,
                headers=headers,
                url=url,
                **kwargs,
            )
        )

    @classmethod
    def patch(
        cls,
        url: str,
        data: Dict[str, Any] = {},
        headers: Dict[str, Any] = {},
        **kwargs,
    ) -> HTTPResponse:
        """
        Make a PATCH request to the specified URL.

        :param url: The URL to make the PATCH request to.
        :type url: str
        :param data: The data to send with the PATCH request.
        :type data: Dict[str, Any]
        :param headers: The headers to send with the PATCH request.
        :type headers: Dict[str, Any]
        :param kwargs: Additional keyword arguments to pass to the PATCH request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __patch__(
            url: str,
            data: Dict[str, Any] = {},
            headers: Dict[str, Any] = {},
            **kwargs,
        ) -> HTTPResponse:
            """
            Make a PATCH request to the specified URL.

            :param url: The URL to make the PATCH request to.
            :type url: str
            :param data: The data to send with the PATCH request.
            :type data: Dict[str, Any]
            :param headers: The headers to send with the PATCH request.
            :type headers: Dict[str, Any]
            :param kwargs: Additional keyword arguments to pass to the PATCH request.
            :type kwargs: Dict[str, Any]

            :return: The HTTPResponse object.
            :rtype: HTTPResponse
            """

            # Initialize the builder
            builder: HTTPResponseBuilder = HTTPResponseBuilder()

            # Set the method of the response
            builder.with_method(value=HTTPMethod.PATCH)

            # Set the URL of the response
            builder.with_url(value=url)

            # Set the headers of the response
            builder.with_headers(value=headers)

            # Set the start time of the response
            builder.with_start(value=datetime.now())

            async with aiohttp.ClientSession() as session:
                async with session.patch(
                    url,
                    headers=headers,
                    data=data,
                    **kwargs,
                ) as response:
                    # Raise an exception if the response is not successful
                    response.raise_for_status()

                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=str.JSON)

                    # Set the message of the response
                    builder.with_message(value=response.reason)

                    builder.with_body(
                        await cls._handle_content_type(
                            content_type=response.content_type,
                            response=response,
                        )
                    )

                    # Set the end time of the response
                    builder.with_end(value=datetime.now())

            # Return the HTTPResponse object
            return builder.build()

        # Return the HTTPResponse object
        return asyncio.run(
            __patch__(
                data=data,
                headers=headers,
                url=url,
                **kwargs,
            )
        )

    @classmethod
    def options(
        cls,
        url: str,
        headers: Dict[str, Any] = {},
        **kwargs,
    ) -> HTTPResponse:
        """
        Make an OPTIONS request to the specified URL.

        :param url: The URL to make the OPTIONS request to.
        :type url: str
        :param headers: The headers to send with the OPTIONS request.
        :type headers: Dict[str, Any]
        :param kwargs: Additional keyword arguments to pass to the OPTIONS request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __options__(
            url: str,
            headers: Dict[str, Any] = {},
            **kwargs,
        ) -> HTTPResponse:
            """
            Make an OPTIONS request to the specified URL.

            :param url: The URL to make the OPTIONS request to.
            :type url: str
            :param headers: The headers to send with the OPTIONS request.
            :type headers: Dict[str, Any]
            :param kwargs: Additional keyword arguments to pass to the OPTIONS request.
            :type kwargs: Dict[str, Any]

            :return: The HTTPResponse object.
            :rtype: HTTPResponse
            """

            # Initialize the builder
            builder: HTTPResponseBuilder = HTTPResponseBuilder()

            # Set the method of the response
            builder.with_method(value=HTTPMethod.OPTIONS)

            # Set the URL of the response
            builder.with_url(value=url)

            # Set the headers of the response
            builder.with_headers(value=headers)

            # Set the start time of the response
            builder.with_start(value=datetime.now())

            async with aiohttp.ClientSession() as session:
                async with session.options(
                    url,
                    headers=headers,
                    **kwargs,
                ) as response:
                    # Raise an exception if the response is not successful
                    response.raise_for_status()

                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=str.JSON)

                    # Set the message of the response
                    builder.with_message(value=response.reason)

                    builder.with_body(
                        await cls._handle_content_type(
                            content_type=response.content_type,
                            response=response,
                        )
                    )

                    # Set the end time of the response
                    builder.with_end(value=datetime.now())

            # Return the HTTPResponse object
            return builder.build()

        # Return the HTTPResponse object
        return asyncio.run(
            __options__(
                headers=headers,
                url=url,
                **kwargs,
            )
        )

    @classmethod
    def trace(
        cls,
        url: str,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make a TRACE request to the specified URL.

        :param url: The URL to make the TRACE request to.
        :type url: str
        :param kwargs: Additional keyword arguments to pass to the TRACE request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __trace__(
            url: str,
            headers: Dict[str, Any] = {},
            **kwargs,
        ) -> HTTPResponse:
            """
            Make a TRACE request to the specified URL.

            :param url: The URL to make the TRACE request to.
            :type url: str
            :param kwargs: Additional keyword arguments to pass to the TRACE request.
            :type kwargs: Dict[str, Any]

            :return: The HTTPResponse object.
            :rtype: HTTPResponse
            """

            # Initialize the builder
            builder: HTTPResponseBuilder = HTTPResponseBuilder()

            # Set the method of the response
            builder.with_method(value=HTTPMethod.TRACE)

            # Set the URL of the response
            builder.with_url(value=url)

            # Set the start time of the response
            builder.with_start(value=datetime.now())

            async with aiohttp.ClientSession() as session:
                async with session.trace(
                    url,
                    **kwargs,
                ) as response:
                    # Raise an exception if the response is not successful
                    response.raise_for_status()

                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=str.JSON)

                    # Set the message of the response
                    builder.with_message(value=response.reason)

                    builder.with_body(
                        await cls._handle_content_type(
                            content_type=response.content_type,
                            response=response,
                        )
                    )

                    # Set the end time of the response
                    builder.with_end(value=datetime.now())

            # Return the HTTPResponse object
            return builder.build()

        # Return the HTTPResponse object
        return asyncio.run(
            __trace__(
                url=url,
                **kwargs,
            )
        )


class URLBuilder:
    """
    URLBuilder class.

    This class is used to build the URL configuration.
    """

    def __init__(
        self,
        url: str,
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

    def with_endpoint(
        self,
        value: str,
    ) -> str:
        """
        Set the endpoint of the URL.

        :param value: The endpoint of the URL.
        :type value: str

        :return: The URL with the endpoint.
        :rtype: str
        """

        # Return the URL with the endpoint
        return f"{self._configuration['url']}/{value}"
