"""
Author: Louis Goodnews
Date: 2025-08-08
"""

from datetime import datetime
from typing import Any, Dict, Final, Optional, Self, Union

from .methods import HTTPMethod, HTTPResponseType


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
        type_value: Union[str, HTTPResponseType],
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
        :param type_value: The type of the response (string or HTTPResponseType).
        :type type_value: Union[str, HTTPResponseType]
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

        # Store the type of the response (convert string to HTTPResponseType if needed)
        if isinstance(type_value, str):
            self._type: Final[HTTPResponseType] = HTTPResponseType.from_content_type(
                type_value
            )
        else:
            self._type: Final[HTTPResponseType] = type_value

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
        return (
            f"HTTPResponse(body={self._body}, duration={self._duration}, "
            f"end={self._end}, headers={self._headers}, message={self._message}, "
            f"method={self._method}, start={self._start}, status={self._status}, "
            f"type={self._type}, url={self._url})"
        )

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
    def type(self) -> HTTPResponseType:
        """
        Return the type of the response.

        :return: The type of the response.
        :rtype: HTTPResponseType
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
            "type": self._type.value,
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
        type_value: Union[str, HTTPResponseType],
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
        :param type_value: The type of the response (string or HTTPResponseType).
        :type type_value: Union[str, HTTPResponseType]
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

        # Return the builder to the caller
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
