"""
Author: Louis Goodnews
Date: 2025-08-08
"""


class WebUtilsError(Exception):
    """Base exception for WebUtils errors."""

    pass


class HTTPRequestError(WebUtilsError):
    """Exception raised when an HTTP request fails."""

    pass


class HTTPTimeoutError(WebUtilsError):
    """Exception raised when an HTTP request times out."""

    pass
