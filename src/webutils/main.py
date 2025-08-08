"""
Author: Louis Goodnews
Date: 2025-08-08
"""

from core.core import HTTPService


def main() -> None:
    """ """

    print(
        HTTPService.get(
            url="https://jsonplaceholder.typicode.com/posts/1",
        ).dict()
    )


if __name__ == "__main__":
    main()
