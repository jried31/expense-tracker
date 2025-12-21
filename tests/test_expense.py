import pytest
from datetime import datetime
from src.models.expense import Expense


class TestExpense:
    def test_expense_creation(self):
        """Test creating expense with valid data."""
        expense = Expense(
            amount=50.99,
            category="Food",
            description="Lunch at restaurant"
        )

        assert expense.amount == 50.99
        assert expense.category == "Food"
        assert expense.description == "Lunch at restaurant"
        assert expense.id is not None
        assert expense.date is not None
        assert expense.created_at is not None

    def test_expense_creation_with_all_params(self):
        """Test creating expense with all parameters specified."""
        expense = Expense(
            amount=100,
            category="Transport",
            description="Taxi",
            date="2025-12-20",
            expense_id="exp_test_123",
            created_at="2025-12-20T10:30:00"
        )

        assert expense.amount == 100.0
        assert expense.category == "Transport"
        assert expense.description == "Taxi"
        assert expense.date == "2025-12-20"
        assert expense.id == "exp_test_123"
        assert expense.created_at == "2025-12-20T10:30:00"

    def test_expense_id_generation(self):
        """Test that unique IDs are generated correctly."""
        expense1 = Expense(10, "Food", "Test")
        expense2 = Expense(20, "Food", "Test")

        assert expense1.id.startswith("exp_")
        assert expense2.id.startswith("exp_")
        assert expense1.id != expense2.id
        assert len(expense1.id.split('_')) == 4

    def test_expense_to_dict(self):
        """Test serialization to dictionary."""
        expense = Expense(
            amount=75.50,
            category="Entertainment",
            description="Movie tickets",
            date="2025-12-21",
            expense_id="exp_20251221_120000_abc123",
            created_at="2025-12-21T12:00:00"
        )

        result = expense.to_dict()

        assert result == {
            "id": "exp_20251221_120000_abc123",
            "amount": 75.50,
            "category": "Entertainment",
            "description": "Movie tickets",
            "date": "2025-12-21",
            "created_at": "2025-12-21T12:00:00"
        }

    def test_expense_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "id": "exp_20251221_120000_abc123",
            "amount": 75.50,
            "category": "Entertainment",
            "description": "Movie tickets",
            "date": "2025-12-21",
            "created_at": "2025-12-21T12:00:00"
        }

        expense = Expense.from_dict(data)

        assert expense.id == "exp_20251221_120000_abc123"
        assert expense.amount == 75.50
        assert expense.category == "Entertainment"
        assert expense.description == "Movie tickets"
        assert expense.date == "2025-12-21"
        assert expense.created_at == "2025-12-21T12:00:00"

    def test_expense_str(self):
        """Test string representation."""
        expense = Expense(
            amount=50.99,
            category="Food",
            description="Lunch",
            date="2025-12-21"
        )

        result = str(expense)

        assert "2025-12-21" in result
        assert "Food" in result
        assert "$50.99" in result or "50.99" in result
        assert "Lunch" in result

    def test_expense_validation_negative_amount(self):
        """Test that negative amounts raise ValueError."""
        with pytest.raises(ValueError, match="Amount must be greater than zero"):
            Expense(-10, "Food", "Test")

    def test_expense_validation_zero_amount(self):
        """Test that zero amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount must be greater than zero"):
            Expense(0, "Food", "Test")

    def test_expense_default_date(self):
        """Test that default date is today."""
        expense = Expense(10, "Food", "Test")
        today = datetime.now().strftime("%Y-%m-%d")

        assert expense.date == today

    def test_generate_id_format(self):
        """Test ID generation format."""
        expense_id = Expense.generate_id()

        parts = expense_id.split('_')
        assert len(parts) == 4
        assert parts[0] == "exp"
        assert len(parts[1]) == 8
        assert len(parts[2]) == 6
        assert len(parts[3]) == 6
