"""
Author: Louis Goodnews
Date: 2025-08-08
"""

from .auth import Authorization, AuthorizationBuilder, AuthorizationFactory
from .exceptions import WebUtilsError, HTTPRequestError, HTTPTimeoutError
from .headers import HeaderBuilder
from .methods import HTTPMethod, HTTPResponseType
from .response import (
    HTTPResponse,
    HTTPResponseFactory,
    HTTPResponseBuilder,
)
from .service import HTTPService
from .url import (
    URL,
    URLBuilder,
    URLFactory,
    URLQuery,
    URLQueryFactory,
    URLQueryBuilder,
)

__all__ = [
    "Authorization",
    "AuthorizationBuilder",
    "AuthorizationFactory",
    "HeaderBuilder",
    "HTTPMethod",
    "HTTPResponseType",
    "HTTPResponse",
    "HTTPResponseFactory",
    "HTTPResponseBuilder",
    "HTTPService",
    "URL",
    "URLBuilder",
    "URLFactory",
    "URLQuery",
    "URLQueryFactory",
    "URLQueryBuilder",
    "WebUtilsError",
    "HTTPRequestError",
    "HTTPTimeoutError",
]
