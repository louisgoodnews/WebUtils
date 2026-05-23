"""
Author: Louis Goodnews
Date: 2025-08-08
"""

from enum import Enum


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


class HTTPResponseType(Enum):
    """
    HTTP Response Type enum.

    This class is used to represent the content type of the HTTP response.

    :cvar JSON: JSON content type.
    :cvar XML: XML content type.
    :cvar TEXT: Text content type.
    :cvar BINARY: Binary content type.
    :cvar IMAGE: Image content type.
    :cvar HTML: HTML content type.
    :cvar UNKNOWN: Unknown content type.
    """

    JSON = "application/json"
    XML = "application/xml"
    TEXT = "text/plain"
    BINARY = "application/octet-stream"
    IMAGE = "image/*"
    HTML = "text/html"
    UNKNOWN = "unknown"

    @classmethod
    def from_content_type(cls, content_type: str) -> "HTTPResponseType":
        """
        Get HTTPResponseType from content type string.

        :param content_type: The content type string.
        :type content_type: str

        :return: The corresponding HTTPResponseType.
        :rtype: HTTPResponseType
        """
        if not content_type:
            return cls.UNKNOWN

        content_type_lower = content_type.lower()

        if "application/json" in content_type_lower:
            return cls.JSON
        elif (
            "application/xml" in content_type_lower or "text/xml" in content_type_lower
        ):
            return cls.XML
        elif "text/plain" in content_type_lower:
            return cls.TEXT
        elif "application/octet-stream" in content_type_lower:
            return cls.BINARY
        elif content_type_lower.startswith("image/"):
            return cls.IMAGE
        elif "text/html" in content_type_lower:
            return cls.HTML
        else:
            return cls.UNKNOWN

    def __str__(self) -> str:
        """
        Return the value of the enum member.

        :return: The value of the enum member.
        :rtype: str
        """

        # Return the value of the enum member
        return self.value
