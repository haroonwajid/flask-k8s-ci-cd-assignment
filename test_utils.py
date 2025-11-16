"""Unit tests for utility functions."""

import pytest
from utils import add_numbers, multiply_numbers, greet


class TestMathOperations:
    """Test mathematical operations."""

    def test_add_numbers_positive(self):
        """Test addition with positive numbers."""
        assert add_numbers(2, 3) == 5

    def test_add_numbers_negative(self):
        """Test addition with negative numbers."""
        assert add_numbers(-2, -3) == -5

    def test_add_numbers_mixed(self):
        """Test addition with mixed sign numbers."""
        assert add_numbers(10, -5) == 5

    def test_multiply_numbers_positive(self):
        """Test multiplication with positive numbers."""
        assert multiply_numbers(3, 4) == 12

    def test_multiply_numbers_with_zero(self):
        """Test multiplication with zero."""
        assert multiply_numbers(5, 0) == 0

    def test_multiply_numbers_negative(self):
        """Test multiplication with negative numbers."""
        assert multiply_numbers(-3, 4) == -12


class TestGreetFunction:
    """Test greeting function."""

    def test_greet_with_name(self):
        """Test greeting with a name."""
        result = greet("Alice")
        assert result == "Hello, Alice!"

    def test_greet_with_empty_string(self):
        """Test greeting with empty string."""
        result = greet("")
        assert result == "Hello, !"

    def test_greet_with_special_characters(self):
        """Test greeting with special characters."""
        result = greet("Bob-O'Brien")
        assert result == "Hello, Bob-O'Brien!"
