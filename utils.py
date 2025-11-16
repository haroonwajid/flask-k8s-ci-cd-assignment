"""Utility functions for the Flask application."""


def add_numbers(a, b):
    """
    Add two numbers and return the result.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    return a + b


def multiply_numbers(a, b):
    """
    Multiply two numbers and return the result.

    Args:
        a: First number
        b: Second number

    Returns:
        The product of a and b
    """
    return a * b


def greet(name):
    """
    Generate a greeting message.

    Args:
        name: Name of the person to greet

    Returns:
        A greeting string
    """
    return f"Hello, {name}!"
