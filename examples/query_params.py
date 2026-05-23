"""
Author: Louis Goodnews
Date: 2025-08-08

Example demonstrating URLQuery, URLQueryFactory, and URLQueryBuilder usage.
"""

from webutils import URLQuery, URLQueryFactory, URLQueryBuilder, URLBuilder


def example_url_query_basic():
    """Basic URLQuery usage."""
    print("=== Basic URLQuery Usage ===")
    
    # Create URLQuery from params dictionary
    query = URLQuery(params={"key": "value", "page": "1"})
    print(f"Query string: {str(query)}")
    
    # Add a parameter
    query.add("tag", "python")
    print(f"After adding tag: {str(query)}")
    
    # Get parameter values
    print(f"Key value: {query.get_first('key')}")
    print(f"Page value: {query.get_first('page')}")
    
    # Check if parameter exists
    print(f"Has 'key': {query.has('key')}")
    print(f"Has 'nonexistent': {query.has('nonexistent')}")
    
    print()


def example_url_query_multiple_values():
    """URLQuery with multiple values for same parameter."""
    print("=== Multiple Values for Same Parameter ===")
    
    query = URLQuery()
    query.add("tag", "python")
    query.add("tag", "web")
    query.add("tag", "api")
    
    print(f"Query string: {str(query)}")
    print(f"All tag values: {query['tag']}")
    print(f"First tag value: {query.get_first('tag')}")
    
    print()


def example_url_query_builder():
    """URLQueryBuilder for fluent API."""
    print("=== URLQueryBuilder Fluent API ===")
    
    query = (URLQueryBuilder()
             .add_param("key", "value")
             .add_param("page", "1")
             .add_param("tag", "python")
             .add_param("tag", "web")
             .build())
    
    print(f"Query string: {str(query)}")
    print(f"Parameters: {query.to_dict()}")
    
    print()


def example_url_query_factory():
    """URLQueryFactory for creating URLQuery objects."""
    print("=== URLQueryFactory ===")
    
    # From query string
    query = URLQueryFactory.create_query("key=value&page=1")
    print(f"From query string: {str(query)}")
    
    # From params dictionary
    query = URLQueryFactory.from_params({"key": "value", "page": "1"})
    print(f"From params dict: {str(query)}")
    
    # From URL string
    query = URLQueryFactory.from_url("https://example.com?key=value&page=1")
    print(f"From URL: {str(query)}")
    
    print()


def example_url_builder_with_query():
    """URLBuilder with query parameters."""
    print("=== URLBuilder with Query Parameters ===")
    
    # Using with_query method
    url = (URLBuilder("https://api.example.com")
           .with_endpoint("search")
           .with_query(q="python", page=1, limit=10)
           .build())
    print(f"URL with query: {str(url)}")
    
    # Using with_query_builder method
    query_builder = (URLQueryBuilder()
                     .add_param("q", "python")
                     .add_param("page", "1")
                     .add_param("limit", "10"))
    
    url = (URLBuilder("https://api.example.com")
           .with_endpoint("search")
           .with_query_builder(query_builder)
           .build())
    print(f"URL with query builder: {str(url)}")
    
    print()


def example_url_query_manipulation():
    """URLQuery manipulation methods."""
    print("=== URLQuery Manipulation ===")
    
    query = URLQuery(params={"key": "value", "page": "1"})
    print(f"Initial: {str(query)}")
    
    # Set parameter (overwrites)
    query.set("page", "2")
    print(f"After set page=2: {str(query)}")
    
    # Remove parameter
    query.remove("key")
    print(f"After remove key: {str(query)}")
    
    # Clear all
    query.clear()
    print(f"After clear: {str(query)}")
    
    print()


def example_url_query_iteration():
    """Iterating over URLQuery parameters."""
    print("=== URLQuery Iteration ===")
    
    query = URLQuery(params={"key": "value", "page": "1", "tag": "python"})
    
    # Iterate over keys
    print("Parameter keys:")
    for key in query:
        print(f"  - {key}: {query.get_first(key)}")
    
    # Check length
    print(f"Number of parameters: {len(query)}")
    
    print()


if __name__ == "__main__":
    example_url_query_basic()
    example_url_query_multiple_values()
    example_url_query_builder()
    example_url_query_factory()
    example_url_builder_with_query()
    example_url_query_manipulation()
    example_url_query_iteration()
