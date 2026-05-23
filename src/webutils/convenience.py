"""
Author: Louis Goodnews
Date: 2025-08-08

Top-level convenience functions for HTTP requests.
"""

from typing import Any, Dict, Iterable, Optional

from .core.service import HTTPResponse, HTTPService


def get(
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
    return HTTPService.get(
        url=url,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def post(
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
    return HTTPService.post(
        url=url,
        data=data,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def put(
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
    return HTTPService.put(
        url=url,
        data=data,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def delete(
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
    return HTTPService.delete(
        url=url,
        data=data,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def patch(
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
    return HTTPService.patch(
        url=url,
        data=data,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def options(
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
    return HTTPService.options(
        url=url,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def trace(
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
    return HTTPService.trace(
        url=url,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def head(
    url: str,
    headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None,
    max_retries: Optional[int] = None,
    retry_delay: Optional[float] = None,
    **kwargs,
) -> HTTPResponse:
    """
    Make a HEAD request to the specified URL.

    :param url: The URL to make the HEAD request to.
    :type url: str
    :param headers: The headers to send with the HEAD request.
    :type headers: Dict[str, Any]
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
    return HTTPService.head(
        url=url,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def bulk_get(
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
    return HTTPService.bulk_get(
        urls=urls,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def bulk_post(
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
    return HTTPService.bulk_post(
        urls=urls,
        data=data,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def bulk_put(
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
    return HTTPService.bulk_put(
        urls=urls,
        data=data,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def bulk_delete(
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
    return HTTPService.bulk_delete(
        urls=urls,
        data=data,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def bulk_patch(
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
    return HTTPService.bulk_patch(
        urls=urls,
        data=data,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def bulk_options(
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
    return HTTPService.bulk_options(
        urls=urls,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def bulk_head(
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
    return HTTPService.bulk_head(
        urls=urls,
        headers=headers,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        **kwargs,
    )


def configure(
    timeout: Optional[float] = None,
    max_retries: Optional[int] = None,
    retry_delay: Optional[float] = None,
) -> None:
    """
    Configure the default timeout and retry settings for HTTP requests.

    :param timeout: Default timeout in seconds.
    :type timeout: Optional[float]
    :param max_retries: Default maximum number of retry attempts.
    :type max_retries: Optional[int]
    :param retry_delay: Default initial delay between retries in seconds.
    :type retry_delay: Optional[float]

    :return: None
    :rtype: None
    """
    HTTPService.configure(
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
    )


def close_session() -> None:
    """
    Close the shared ClientSession.

    :return: None
    :rtype: None
    """
    import asyncio

    asyncio.run(HTTPService.close_session())
