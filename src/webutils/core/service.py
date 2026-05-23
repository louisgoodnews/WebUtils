"""
Author: Louis Goodnews
Date: 2025-08-08
"""

import aiohttp
import asyncio
import concurrent.futures
from datetime import datetime
from typing import Any, Dict, Iterable, Optional, Union

from .exceptions import HTTPRequestError, HTTPTimeoutError
from .methods import HTTPMethod, HTTPResponseType
from .response import HTTPResponse, HTTPResponseBuilder


class HTTPService:
    """
    A service class to make HTTP requests to the specified URL.
    """

    _session: Optional[aiohttp.ClientSession] = None
    _default_timeout: float = 30.0
    _default_max_retries: int = 3
    _default_retry_delay: float = 1.0

    @classmethod
    def configure(
        cls,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
    ) -> None:
        """
        Configure default timeout and retry settings.

        :param timeout: Default timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]

        :return: None
        :rtype: None
        """
        if timeout is not None:
            cls._default_timeout = timeout
        if max_retries is not None:
            cls._default_max_retries = max_retries
        if retry_delay is not None:
            cls._default_retry_delay = retry_delay

    @classmethod
    def _get_session(cls) -> aiohttp.ClientSession:
        """
        Get or create a shared ClientSession for connection pooling.

        :return: The ClientSession instance.
        :rtype: aiohttp.ClientSession
        """
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession()
        return cls._session

    @classmethod
    async def close_session(cls) -> None:
        """
        Close the shared ClientSession.

        :return: None
        :rtype: None
        """
        if cls._session is not None and not cls._session.closed:
            await cls._session.close()
            cls._session = None

    @classmethod
    async def _retry_request(
        cls,
        request_func,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
    ) -> HTTPResponse:
        """
        Retry a request with exponential backoff.

        :param request_func: The async function to execute.
        :type request_func: Callable
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """
        max_retries = max_retries or cls._default_max_retries
        retry_delay = retry_delay or cls._default_retry_delay

        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                return await request_func()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_exception = e
                if attempt < max_retries:
                    await asyncio.sleep(retry_delay * (2**attempt))
                else:
                    if isinstance(e, asyncio.TimeoutError):
                        raise HTTPTimeoutError(
                            f"Request failed after {max_retries} retries: {e}"
                        ) from e
                    else:
                        raise HTTPRequestError(
                            f"Request failed after {max_retries} retries: {e}"
                        ) from e

        raise HTTPRequestError(f"Request failed: {last_exception}") from last_exception

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
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make a GET request to the specified URL.

        :param url: The URL to make the GET request to.
        :type url: str
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the GET request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __get__(
            url: str,
            timeout: Optional[float],
            **kwargs,
        ) -> HTTPResponse:
            """
            Make a GET request to the specified URL.

            :param url: The URL to make the GET request to.
            :type url: str
            :param timeout: Request timeout in seconds.
            :type timeout: Optional[float]
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

            timeout = timeout or cls._default_timeout
            try:
                session = cls._get_session()
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    **kwargs,
                ) as response:
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
            except aiohttp.ClientError as e:
                raise HTTPRequestError(f"HTTP request failed: {e}") from e
            except asyncio.TimeoutError as e:
                raise HTTPTimeoutError(f"Request timed out: {e}") from e

            # Return the HTTPResponse object
            return builder.build()

        async def __get_with_retry() -> HTTPResponse:
            return await cls._retry_request(
                lambda: __get__(url, timeout, **kwargs),
                max_retries=max_retries,
                retry_delay=retry_delay,
            )

        # Return the HTTPResponse object
        return asyncio.run(__get_with_retry())

    @classmethod
    def post(
        cls,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
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
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the POST request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __post__(
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            timeout: Optional[float] = None,
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

            timeout = timeout or cls._default_timeout
            try:
                session = cls._get_session()
                async with session.post(
                    url,
                    headers=headers,
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    **kwargs,
                ) as response:
                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=response.content_type)

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
            except aiohttp.ClientError as e:
                raise HTTPRequestError(f"HTTP request failed: {e}") from e
            except asyncio.TimeoutError as e:
                raise HTTPTimeoutError(f"Request timed out: {e}") from e

            # Return the HTTPResponse object
            return builder.build()

        async def __post_with_retry() -> HTTPResponse:
            return await cls._retry_request(
                lambda: __post__(url, data or {}, headers or {}, timeout, **kwargs),
                max_retries=max_retries,
                retry_delay=retry_delay,
            )

        # Return the HTTPResponse object
        return asyncio.run(__post_with_retry())

    @classmethod
    def put(
        cls,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
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
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the PUT request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __put__(
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            timeout: Optional[float] = None,
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

            timeout = timeout or cls._default_timeout
            try:
                session = cls._get_session()
                async with session.put(
                    url,
                    headers=headers,
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    **kwargs,
                ) as response:
                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=response.content_type)

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
            except aiohttp.ClientError as e:
                raise HTTPRequestError(f"HTTP request failed: {e}") from e
            except asyncio.TimeoutError as e:
                raise HTTPTimeoutError(f"Request timed out: {e}") from e

            # Return the HTTPResponse object
            return builder.build()

        async def __put_with_retry() -> HTTPResponse:
            return await cls._retry_request(
                lambda: __put__(url, data or {}, headers or {}, timeout, **kwargs),
                max_retries=max_retries,
                retry_delay=retry_delay,
            )

        # Return the HTTPResponse object
        return asyncio.run(__put_with_retry())

    @classmethod
    def delete(
        cls,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
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
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the DELETE request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __delete__(
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            timeout: Optional[float] = None,
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

            try:
                session = cls._get_session()
                async with session.delete(
                    url,
                    headers=headers,
                    data=data,
                    **kwargs,
                ) as response:
                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=response.content_type)

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
            except aiohttp.ClientError as e:
                raise HTTPRequestError(f"HTTP request failed: {e}") from e
            except asyncio.TimeoutError as e:
                raise HTTPTimeoutError(f"Request timed out: {e}") from e

            # Return the HTTPResponse object
            return builder.build()

        async def __delete_with_retry() -> HTTPResponse:
            return await cls._retry_request(
                lambda: __delete__(url, data or {}, headers or {}, timeout, **kwargs),
                max_retries=max_retries,
                retry_delay=retry_delay,
            )

        # Return the HTTPResponse object
        return asyncio.run(__delete_with_retry())

    @classmethod
    def patch(
        cls,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
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
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the PATCH request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __patch__(
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            timeout: Optional[float] = None,
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

            timeout = timeout or cls._default_timeout
            try:
                session = cls._get_session()
                async with session.patch(
                    url,
                    headers=headers,
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    **kwargs,
                ) as response:
                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=response.content_type)

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
            except aiohttp.ClientError as e:
                raise HTTPRequestError(f"HTTP request failed: {e}") from e
            except asyncio.TimeoutError as e:
                raise HTTPTimeoutError(f"Request timed out: {e}") from e

            # Return the HTTPResponse object
            return builder.build()

        async def __patch_with_retry() -> HTTPResponse:
            return await cls._retry_request(
                lambda: __patch__(url, data or {}, headers or {}, timeout, **kwargs),
                max_retries=max_retries,
                retry_delay=retry_delay,
            )

        # Return the HTTPResponse object
        return asyncio.run(__patch_with_retry())

    @classmethod
    def options(
        cls,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make an OPTIONS request to the specified URL.

        :param url: The URL to make the OPTIONS request to.
        :type url: str
        :param headers: The headers to send with the OPTIONS request.
        :type headers: Dict[str, Any]
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the OPTIONS request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __options__(
            url: str,
            headers: Optional[Dict[str, Any]] = None,
            timeout: Optional[float] = None,
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

            timeout = timeout or cls._default_timeout
            try:
                session = cls._get_session()
                async with session.options(
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    **kwargs,
                ) as response:
                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=response.content_type)

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
            except aiohttp.ClientError as e:
                raise HTTPRequestError(f"HTTP request failed: {e}") from e
            except asyncio.TimeoutError as e:
                raise HTTPTimeoutError(f"Request timed out: {e}") from e

            # Return the HTTPResponse object
            return builder.build()

        async def __options_with_retry() -> HTTPResponse:
            return await cls._retry_request(
                lambda: __options__(url, headers or {}, timeout, **kwargs),
                max_retries=max_retries,
                retry_delay=retry_delay,
            )

        # Return the HTTPResponse object
        return asyncio.run(__options_with_retry())

    @classmethod
    def trace(
        cls,
        url: str,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make a TRACE request to the specified URL.

        :param url: The URL to make the TRACE request to.
        :type url: str
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the TRACE request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __trace__(
            url: str,
            timeout: Optional[float] = None,
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

            timeout = timeout or cls._default_timeout
            try:
                session = cls._get_session()
                async with session.trace(
                    url,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    **kwargs,
                ) as response:
                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=response.content_type)

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
            except aiohttp.ClientError as e:
                raise HTTPRequestError(f"HTTP request failed: {e}") from e
            except asyncio.TimeoutError as e:
                raise HTTPTimeoutError(f"Request timed out: {e}") from e

            # Return the HTTPResponse object
            return builder.build()

        async def __trace_with_retry() -> HTTPResponse:
            return await cls._retry_request(
                lambda: __trace__(url, timeout, **kwargs),
                max_retries=max_retries,
                retry_delay=retry_delay,
            )

        # Return the HTTPResponse object
        return asyncio.run(__trace_with_retry())

    @classmethod
    def head(
        cls,
        url: str,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make a HEAD request to the specified URL.

        :param url: The URL to make the HEAD request to.
        :type url: str
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the HEAD request.
        :type kwargs: Dict[str, Any]

        :return: The HTTPResponse object.
        :rtype: HTTPResponse
        """

        async def __head__(
            url: str,
            headers: Optional[Dict[str, Any]] = None,
            timeout: Optional[float] = None,
            **kwargs,
        ) -> HTTPResponse:
            """
            Make a HEAD request to the specified URL.

            :param url: The URL to make the HEAD request to.
            :type url: str
            :param kwargs: Additional keyword arguments to pass to the HEAD request.
            :type kwargs: Dict[str, Any]

            :return: The HTTPResponse object.
            :rtype: HTTPResponse
            """

            # Initialize the builder
            builder: HTTPResponseBuilder = HTTPResponseBuilder()

            # Set the method of the response
            builder.with_method(value=HTTPMethod.HEAD)

            # Set the headers of the response
            builder.with_headers(value=headers)

            # Set the URL of the response
            builder.with_url(value=url)

            # Set the start time of the response
            builder.with_start(value=datetime.now())

            timeout = timeout or cls._default_timeout
            try:
                session = cls._get_session()
                async with session.head(
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    **kwargs,
                ) as response:
                    # Set the status of the response
                    builder.with_status(value=response.status)

                    # Set the type of the response
                    builder.with_type(value=response.content_type)

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
            except aiohttp.ClientError as e:
                raise HTTPRequestError(f"HTTP request failed: {e}") from e
            except asyncio.TimeoutError as e:
                raise HTTPTimeoutError(f"Request timed out: {e}") from e

            # Return the HTTPResponse object
            return builder.build()

        async def __head_with_retry() -> HTTPResponse:
            request_headers = kwargs.get("headers", {}) or {}
            return await cls._retry_request(
                lambda: __head__(url, request_headers, timeout, **kwargs),
                max_retries=max_retries,
                retry_delay=retry_delay,
            )

        # Return the HTTPResponse object
        return asyncio.run(__head_with_retry())

    @classmethod
    def bulk_get(
        cls,
        urls: Iterable[str],
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make multiple GET requests concurrently using threading.

        :param urls: An iterable of URLs to make GET requests to.
        :type urls: Iterable[str]
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the GET requests.
        :type kwargs: Dict[str, Any]

        :return: A single HTTPResponse object with body containing results.
        :rtype: HTTPResponse
        """

        def _get_single(url: str) -> HTTPResponse:
            return cls.get(
                url,
                timeout=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay,
                **kwargs,
            )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(_get_single, url) for url in urls]
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response.dict())
                except Exception as e:
                    error_dict = {"error": str(e)}
                    results.append(error_dict)

        # Create a bulk response
        builder = HTTPResponseBuilder()
        builder.with_method(HTTPMethod.GET)
        builder.with_status(200)
        builder.with_message("Bulk request completed")
        builder.with_type(HTTPResponseType.JSON)
        builder.with_body({"results": results})
        builder.with_start(datetime.now())
        builder.with_end(datetime.now())
        builder.with_headers({})
        builder.with_url("bulk://get")

        return builder.build()

    @classmethod
    def bulk_post(
        cls,
        urls: Iterable[str],
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make multiple POST requests concurrently using threading.

        :param urls: An iterable of URLs to make POST requests to.
        :type urls: Iterable[str]
        :param data: The data to send with the POST requests.
        :type data: Dict[str, Any]
        :param headers: The headers to send with the POST requests.
        :type headers: Dict[str, Any]
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the POST requests.
        :type kwargs: Dict[str, Any]

        :return: A single HTTPResponse object with body containing results.
        :rtype: HTTPResponse
        """

        def _post_single(url: str) -> HTTPResponse:
            return cls.post(
                url,
                data=data,
                headers=headers,
                timeout=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay,
                **kwargs,
            )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(_post_single, url) for url in urls]
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response.dict())
                except Exception as e:
                    results.append({"error": str(e)})

        # Create a bulk response
        builder = HTTPResponseBuilder()
        builder.with_method(HTTPMethod.POST)
        builder.with_status(200)
        builder.with_message("Bulk request completed")
        builder.with_type(HTTPResponseType.JSON)
        builder.with_body({"results": results})
        builder.with_start(datetime.now())
        builder.with_end(datetime.now())
        builder.with_headers(headers or {})
        builder.with_url("bulk://post")

        return builder.build()

    @classmethod
    def bulk_put(
        cls,
        urls: Iterable[str],
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make multiple PUT requests concurrently using threading.

        :param urls: An iterable of URLs to make PUT requests to.
        :type urls: Iterable[str]
        :param data: The data to send with the PUT requests.
        :type data: Dict[str, Any]
        :param headers: The headers to send with the PUT requests.
        :type headers: Dict[str, Any]
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the PUT requests.
        :type kwargs: Dict[str, Any]

        :return: A single HTTPResponse object with body containing results.
        :rtype: HTTPResponse
        """

        def _put_single(url: str) -> HTTPResponse:
            return cls.put(
                url,
                data=data,
                headers=headers,
                timeout=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay,
                **kwargs,
            )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(_put_single, url) for url in urls]
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response.dict())
                except Exception as e:
                    results.append({"error": str(e)})

        # Create a bulk response
        builder = HTTPResponseBuilder()
        builder.with_method(HTTPMethod.PUT)
        builder.with_status(200)
        builder.with_message("Bulk request completed")
        builder.with_type(HTTPResponseType.JSON)
        builder.with_body({"results": results})
        builder.with_start(datetime.now())
        builder.with_end(datetime.now())
        builder.with_headers(headers or {})
        builder.with_url("bulk://put")

        return builder.build()

    @classmethod
    def bulk_delete(
        cls,
        urls: Iterable[str],
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make multiple DELETE requests concurrently using threading.

        :param urls: An iterable of URLs to make DELETE requests to.
        :type urls: Iterable[str]
        :param data: The data to send with the DELETE requests.
        :type data: Dict[str, Any]
        :param headers: The headers to send with the DELETE requests.
        :type headers: Dict[str, Any]
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the DELETE requests.
        :type kwargs: Dict[str, Any]

        :return: A single HTTPResponse object with body containing results.
        :rtype: HTTPResponse
        """

        def _delete_single(url: str) -> HTTPResponse:
            return cls.delete(
                url,
                data=data,
                headers=headers,
                timeout=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay,
                **kwargs,
            )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(_delete_single, url) for url in urls]
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response.dict())
                except Exception as e:
                    results.append({"error": str(e)})

        # Create a bulk response
        builder = HTTPResponseBuilder()
        builder.with_method(HTTPMethod.DELETE)
        builder.with_status(200)
        builder.with_message("Bulk request completed")
        builder.with_type(HTTPResponseType.JSON)
        builder.with_body({"results": results})
        builder.with_start(datetime.now())
        builder.with_end(datetime.now())
        builder.with_headers(headers or {})
        builder.with_url("bulk://delete")

        return builder.build()

    @classmethod
    def bulk_patch(
        cls,
        urls: Iterable[str],
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make multiple PATCH requests concurrently using threading.

        :param urls: An iterable of URLs to make PATCH requests to.
        :type urls: Iterable[str]
        :param data: The data to send with the PATCH requests.
        :type data: Dict[str, Any]
        :param headers: The headers to send with the PATCH requests.
        :type headers: Dict[str, Any]
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the PATCH requests.
        :type kwargs: Dict[str, Any]

        :return: A single HTTPResponse object with body containing results.
        :rtype: HTTPResponse
        """

        def _patch_single(url: str) -> HTTPResponse:
            return cls.patch(
                url,
                data=data,
                headers=headers,
                timeout=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay,
                **kwargs,
            )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(_patch_single, url) for url in urls]
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response.dict())
                except Exception as e:
                    results.append({"error": str(e)})

        # Create a bulk response
        builder = HTTPResponseBuilder()
        builder.with_method(HTTPMethod.PATCH)
        builder.with_status(200)
        builder.with_message("Bulk request completed")
        builder.with_type(HTTPResponseType.JSON)
        builder.with_body({"results": results})
        builder.with_start(datetime.now())
        builder.with_end(datetime.now())
        builder.with_headers(headers or {})
        builder.with_url("bulk://patch")

        return builder.build()

    @classmethod
    def bulk_options(
        cls,
        urls: Iterable[str],
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make multiple OPTIONS requests concurrently using threading.

        :param urls: An iterable of URLs to make OPTIONS requests to.
        :type urls: Iterable[str]
        :param headers: The headers to send with the OPTIONS requests.
        :type headers: Dict[str, Any]
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the OPTIONS requests.
        :type kwargs: Dict[str, Any]

        :return: A single HTTPResponse object with body containing results.
        :rtype: HTTPResponse
        """

        def _options_single(url: str) -> HTTPResponse:
            return cls.options(
                url,
                headers=headers,
                timeout=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay,
                **kwargs,
            )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(_options_single, url) for url in urls]
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response.dict())
                except Exception as e:
                    results.append({"error": str(e)})

        # Create a bulk response
        builder = HTTPResponseBuilder()
        builder.with_method(HTTPMethod.OPTIONS)
        builder.with_status(200)
        builder.with_message("Bulk request completed")
        builder.with_type(HTTPResponseType.JSON)
        builder.with_body({"results": results})
        builder.with_start(datetime.now())
        builder.with_end(datetime.now())
        builder.with_headers(headers or {})
        builder.with_url("bulk://options")

        return builder.build()

    @classmethod
    def bulk_head(
        cls,
        urls: Iterable[str],
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        **kwargs,
    ) -> HTTPResponse:
        """
        Make multiple HEAD requests concurrently using threading.

        :param urls: An iterable of URLs to make HEAD requests to.
        :type urls: Iterable[str]
        :param headers: The headers to send with the HEAD requests.
        :type headers: Dict[str, Any]
        :param timeout: Request timeout in seconds.
        :type timeout: Optional[float]
        :param max_retries: Maximum number of retry attempts.
        :type max_retries: Optional[int]
        :param retry_delay: Initial delay between retries in seconds.
        :type retry_delay: Optional[float]
        :param kwargs: Additional keyword arguments to pass to the HEAD requests.
        :type kwargs: Dict[str, Any]

        :return: A single HTTPResponse object with body containing results.
        :rtype: HTTPResponse
        """

        def _head_single(url: str) -> HTTPResponse:
            return cls.head(
                url,
                headers=headers,
                timeout=timeout,
                max_retries=max_retries,
                retry_delay=retry_delay,
                **kwargs,
            )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(_head_single, url) for url in urls]
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response.dict())
                except Exception as e:
                    results.append({"error": str(e)})

        # Create a bulk response
        builder = HTTPResponseBuilder()
        builder.with_method(HTTPMethod.HEAD)
        builder.with_status(200)
        builder.with_message("Bulk request completed")
        builder.with_type(HTTPResponseType.JSON)
        builder.with_body({"results": results})
        builder.with_start(datetime.now())
        builder.with_end(datetime.now())
        builder.with_headers(headers or {})
        builder.with_url("bulk://head")

        return builder.build()
