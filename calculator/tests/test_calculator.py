"""Test suite for the calculator core functionality."""

from calculator.core.calc import Calculator


def test_basic_calculation() -> None:
    """Test basic arithmetic operations."""
    calc = Calculator()
    assert calc.calculate("2 + 2") == 4.0


def test_invalid_characters() -> None:
    """Test handling of invalid input characters."""
    calc = Calculator()
    result = calc.calculate("2 + 2; DROP TABLE users;")
    assert isinstance(result, str)
    assert "Invalid characters" in result


def test_division_by_zero() -> None:
    """Test handling of division by zero."""
    calc = Calculator()
    result = calc.calculate("1/0")
    assert isinstance(result, str)
    assert "Error" in result


def test_complex_expression() -> None:
    """Test handling of complex mathematical expressions."""
    calc = Calculator()
    assert calc.calculate("(2 + 3) * 4") == 20.0 