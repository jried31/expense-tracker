import pytest
from datetime import datetime
from unittest.mock import patch
from src.utils.validators import validate_amount, validate_category, validate_date, get_valid_input


class TestValidateAmount:
    def test_validate_amount_valid(self):
        """Test valid amount inputs."""
        assert validate_amount("50.99") == 50.99
        assert validate_amount("100") == 100.0
        assert validate_amount("0.01") == 0.01
        assert validate_amount("1000.50") == 1000.50

    def test_validate_amount_negative(self):
        """Test that negative amounts raise ValueError."""
        with pytest.raises(ValueError, match="Amount must be greater than zero"):
            validate_amount("-10")

    def test_validate_amount_zero(self):
        """Test that zero amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount must be greater than zero"):
            validate_amount("0")

    def test_validate_amount_invalid_string(self):
        """Test that non-numeric strings raise ValueError."""
        with pytest.raises(ValueError, match="Amount must be a valid number"):
            validate_amount("abc")

        with pytest.raises(ValueError, match="Amount must be a valid number"):
            validate_amount("12.34.56")

    def test_validate_amount_empty(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Amount must be a valid number"):
            validate_amount("")


class TestValidateCategory:
    def test_validate_category_valid(self):
        """Test valid category inputs."""
        assert validate_category("food") == "Food"
        assert validate_category("TRANSPORT") == "Transport"
        assert validate_category("Entertainment") == "Entertainment"
        assert validate_category("  shopping  ") == "Shopping"

    def test_validate_category_empty(self):
        """Test that empty category raises ValueError."""
        with pytest.raises(ValueError, match="Category cannot be empty"):
            validate_category("")

        with pytest.raises(ValueError, match="Category cannot be empty"):
            validate_category("   ")

    def test_validate_category_capitalization(self):
        """Test that category is capitalized."""
        assert validate_category("food") == "Food"
        assert validate_category("food and drinks") == "Food and drinks"


class TestValidateDate:
    def test_validate_date_valid(self):
        """Test valid ISO date inputs."""
        assert validate_date("2025-12-21") == "2025-12-21"
        assert validate_date("2025-01-01") == "2025-01-01"
        assert validate_date("2024-12-31") == "2024-12-31"

    def test_validate_date_empty(self):
        """Test that empty date defaults to today."""
        today = datetime.now().strftime("%Y-%m-%d")
        assert validate_date("") == today
        assert validate_date("   ") == today

    def test_validate_date_invalid_format(self):
        """Test that invalid date formats raise ValueError."""
        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format"):
            validate_date("12/21/2025")

        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format"):
            validate_date("2025-13-01")

        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format"):
            validate_date("2025-12-32")

        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format"):
            validate_date("not a date")

    def test_validate_date_none(self):
        """Test that None defaults to today."""
        today = datetime.now().strftime("%Y-%m-%d")
        assert validate_date(None) == today


class TestGetValidInput:
    def test_get_valid_input_no_validator(self):
        """Test getting input without validation."""
        with patch('builtins.input', return_value='test input'):
            result = get_valid_input("Enter something: ")
            assert result == "test input"

    def test_get_valid_input_with_validator_success(self):
        """Test getting input with successful validation."""
        with patch('builtins.input', return_value='50.99'):
            result = get_valid_input("Enter amount: ", validate_amount)
            assert result == 50.99

    def test_get_valid_input_with_validator_retry(self):
        """Test that invalid input prompts for retry."""
        with patch('builtins.input', side_effect=['-10', '50.99']):
            with patch('builtins.print') as mock_print:
                result = get_valid_input("Enter amount: ", validate_amount)
                assert result == 50.99
                mock_print.assert_called()

    def test_get_valid_input_multiple_retries(self):
        """Test multiple retry attempts."""
        with patch('builtins.input', side_effect=['abc', '-5', '0', '25.50']):
            with patch('builtins.print') as mock_print:
                result = get_valid_input("Enter amount: ", validate_amount)
                assert result == 25.50
                assert mock_print.call_count == 3

    def test_get_valid_input_category_validation(self):
        """Test input validation with category validator."""
        with patch('builtins.input', side_effect=['  ', 'food']):
            with patch('builtins.print'):
                result = get_valid_input("Enter category: ", validate_category)
                assert result == "Food"
