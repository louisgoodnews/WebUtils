"""
Author: Louis Goodnews
Date: 2025-08-08
"""

from typing import Final, List, Literal

from .core import (
    Authorization,
    AuthorizationBuilder,
    AuthorizationFactory,
    HeaderBuilder,
    HTTPMethod,
    HTTPResponseType,
    HTTPResponse,
    HTTPResponseFactory,
    HTTPResponseBuilder,
    HTTPService,
    URL,
    URLBuilder,
    URLFactory,
    URLQuery,
    URLQueryFactory,
    URLQueryBuilder,
    WebUtilsError,
    HTTPRequestError,
    HTTPTimeoutError,
)

# Import top-level convenience functions from convenience module
from .convenience import (
    get,
    post,
    put,
    delete,
    patch,
    options,
    trace,
    head,
    bulk_get,
    bulk_post,
    bulk_put,
    bulk_delete,
    bulk_patch,
    bulk_options,
    bulk_head,
    configure,
    close_session,
)

__all__: Final[List[str]] = [
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
    # Top-level convenience functions
    "get",
    "post",
    "put",
    "delete",
    "patch",
    "options",
    "trace",
    "head",
    "bulk_get",
    "bulk_post",
    "bulk_put",
    "bulk_delete",
    "bulk_patch",
    "bulk_options",
    "bulk_head",
    "configure",
    "close_session",
]

__version__: Final[Literal["0.1.0"]] = "0.1.0"
