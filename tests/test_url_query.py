"""
Tests for URLQuery, URLQueryFactory, and URLQueryBuilder classes.
"""

import pytest

from webutils import URLQuery, URLQueryFactory, URLQueryBuilder


class TestURLQuery:
    """Test cases for URLQuery class."""

    def test_initialization_with_query_string(self):
        """Test URLQuery initialization with query string."""
        query = URLQuery(query="key1=value1&key2=value2")
        assert "key1" in query
        assert "key2" in query
        assert query["key1"] == ["value1"]
        assert query["key2"] == ["value2"]

    def test_initialization_with_params_dict(self):
        """Test URLQuery initialization with params dictionary."""
        query = URLQuery(params={"key1": "value1", "key2": "value2"})
        assert "key1" in query
        assert "key2" in query
        assert query["key1"] == ["value1"]
        assert query["key2"] == ["value2"]

    def test_initialization_empty(self):
        """Test URLQuery initialization with no parameters."""
        query = URLQuery()
        assert len(query) == 0
        assert str(query) == ""

    def test_str_representation(self):
        """Test string representation of URLQuery."""
        query = URLQuery(params={"key": "value"})
        assert str(query) == "key=value"

    def test_repr_representation(self):
        """Test repr representation of URLQuery."""
        query = URLQuery(params={"key": "value"})
        assert repr(query) == "URLQuery('key=value')"

    def test_getitem(self):
        """Test getting parameter values."""
        query = URLQuery(params={"key": "value"})
        assert query["key"] == ["value"]
        assert query["nonexistent"] == []

    def test_setitem(self):
        """Test setting parameter values."""
        query = URLQuery()
        query["key"] = "value"
        assert query["key"] == ["value"]

    def test_delitem(self):
        """Test deleting parameter."""
        query = URLQuery(params={"key": "value"})
        del query["key"]
        assert "key" not in query

    def test_contains(self):
        """Test checking if parameter exists."""
        query = URLQuery(params={"key": "value"})
        assert "key" in query
        assert "nonexistent" not in query

    def test_len(self):
        """Test getting number of parameters."""
        query = URLQuery(params={"key1": "value1", "key2": "value2"})
        assert len(query) == 2

    def test_iteration(self):
        """Test iterating over parameter keys."""
        query = URLQuery(params={"key1": "value1", "key2": "value2"})
        keys = list(query)
        assert "key1" in keys
        assert "key2" in keys

    def test_add_single_value(self):
        """Test adding a single value parameter."""
        query = URLQuery()
        query.add("key", "value")
        assert query["key"] == ["value"]

    def test_add_multiple_values(self):
        """Test adding multiple values to same parameter."""
        query = URLQuery()
        query.add("key", "value1")
        query.add("key", "value2")
        assert query["key"] == ["value1", "value2"]

    def test_set_parameter(self):
        """Test setting a parameter (overwrites existing)."""
        query = URLQuery(params={"key": "old_value"})
        query.set("key", "new_value")
        assert query["key"] == ["new_value"]

    def test_remove_parameter(self):
        """Test removing a parameter."""
        query = URLQuery(params={"key": "value"})
        query.remove("key")
        assert "key" not in query

    def test_get_with_default(self):
        """Test getting parameter with default value."""
        query = URLQuery()
        assert query.get("nonexistent", ["default"]) == ["default"]

    def test_get_first(self):
        """Test getting first value of parameter."""
        query = URLQuery(params={"key": ["value1", "value2"]})
        assert query.get_first("key") == "value1"

    def test_get_first_with_default(self):
        """Test getting first value with default."""
        query = URLQuery()
        assert query.get_first("nonexistent", "default") == "default"

    def test_has(self):
        """Test checking if parameter exists."""
        query = URLQuery(params={"key": "value"})
        assert query.has("key") is True
        assert query.has("nonexistent") is False

    def test_clear(self):
        """Test clearing all parameters."""
        query = URLQuery(params={"key": "value"})
        query.clear()
        assert len(query) == 0

    def test_to_dict(self):
        """Test converting to dictionary."""
        query = URLQuery(params={"key": "value"})
        result = query.to_dict()
        assert result == {"key": "value"}

    def test_to_dict_multiple_values(self):
        """Test converting to dictionary with multiple values."""
        query = URLQuery(params={"key": ["value1", "value2"]})
        result = query.to_dict()
        assert result == {"key": ["value1", "value2"]}

    def test_copy(self):
        """Test copying URLQuery object."""
        query = URLQuery(params={"key": "value"})
        copy = query.copy()
        assert copy["key"] == ["value"]
        copy.set("key", "new_value")
        assert query["key"] == ["value"]


class TestURLQueryFactory:
    """Test cases for URLQueryFactory class."""

    def test_create_query_from_string(self):
        """Test creating URLQuery from query string."""
        query = URLQueryFactory.create_query("key1=value1&key2=value2")
        assert query["key1"] == ["value1"]
        assert query["key2"] == ["value2"]

    def test_from_params(self):
        """Test creating URLQuery from params dictionary."""
        query = URLQueryFactory.from_params({"key": "value"})
        assert query["key"] == ["value"]

    def test_from_url(self):
        """Test creating URLQuery from URL string."""
        query = URLQueryFactory.from_url("https://example.com?key=value")
        assert query["key"] == ["value"]


class TestURLQueryBuilder:
    """Test cases for URLQueryBuilder class."""

    def test_initialization(self):
        """Test URLQueryBuilder initialization."""
        builder = URLQueryBuilder()
        assert builder is not None

    def test_add_param(self):
        """Test adding a parameter."""
        builder = URLQueryBuilder()
        builder.add_param("key", "value")
        query = builder.build()
        assert query["key"] == ["value"]

    def test_set_param(self):
        """Test setting a parameter."""
        builder = URLQueryBuilder()
        builder.set_param("key", "value")
        query = builder.build()
        assert query["key"] == ["value"]

    def test_remove_param(self):
        """Test removing a parameter."""
        builder = URLQueryBuilder()
        builder.set_param("key", "value")
        builder.remove_param("key")
        query = builder.build()
        assert "key" not in query

    def test_clear_params(self):
        """Test clearing all parameters."""
        builder = URLQueryBuilder()
        builder.set_param("key", "value")
        builder.clear_params()
        query = builder.build()
        assert len(query) == 0

    def test_with_params(self):
        """Test setting multiple parameters at once."""
        builder = URLQueryBuilder()
        builder.with_params({"key1": "value1", "key2": "value2"})
        query = builder.build()
        assert query["key1"] == ["value1"]
        assert query["key2"] == ["value2"]

    def test_method_chaining(self):
        """Test method chaining."""
        query = (URLQueryBuilder()
                 .add_param("key1", "value1")
                 .add_param("key2", "value2")
                 .build())
        assert query["key1"] == ["value1"]
        assert query["key2"] == ["value2"]

    def test_build_returns_urlquery(self):
        """Test that build returns URLQuery object."""
        builder = URLQueryBuilder()
        query = builder.build()
        assert isinstance(query, URLQuery)
