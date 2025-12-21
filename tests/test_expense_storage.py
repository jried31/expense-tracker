import pytest
import json
import tempfile
import shutil
from pathlib import Path
from src.models.expense import Expense
from src.storage.expense_storage import ExpenseStorage


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def storage(temp_dir):
    """Create ExpenseStorage instance with temporary directory."""
    return ExpenseStorage(temp_dir)


class TestExpenseStorage:
    def test_ensure_data_directory(self, temp_dir):
        """Test that data directory is created."""
        data_dir = Path(temp_dir) / "test_data"
        storage = ExpenseStorage(str(data_dir))

        assert data_dir.exists()
        assert data_dir.is_dir()

    def test_save_expense(self, storage, temp_dir):
        """Test saving expense to JSON file."""
        expense = Expense(
            amount=50.99,
            category="Food",
            description="Lunch",
            expense_id="exp_20251221_120000_abc123"
        )

        filepath = storage.save_expense(expense)

        assert Path(filepath).exists()
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert data["id"] == "exp_20251221_120000_abc123"
            assert data["amount"] == 50.99
            assert data["category"] == "Food"

    def test_save_negative_expense(self, storage, temp_dir):
        """Test saving expense to JSON file."""

        with pytest.raises(ValueError, match="Amount must be greater than zero"):
            Expense(
                        amount=-50.1,
                        category="Food",
                        description="Lunch",
                        expense_id="exp_20251221_120000_abc123"
                    )

    def test_load_all_expenses(self, storage, temp_dir):
        """Test loading multiple expenses."""
        expense1 = Expense(50, "Food", "Lunch", expense_id="exp_1")
        expense2 = Expense(30, "Transport", "Taxi", expense_id="exp_2")
        expense3 = Expense(100, "Entertainment", "Concert", expense_id="exp_3")

        storage.save_expense(expense1)
        storage.save_expense(expense2)
        storage.save_expense(expense3)

        expenses = storage.load_all_expenses()

        assert len(expenses) == 3
        expense_ids = [e.id for e in expenses]
        assert "exp_1" in expense_ids
        assert "exp_2" in expense_ids
        assert "exp_3" in expense_ids

    def test_load_empty_directory(self, storage):
        """Test loading when no expenses exist."""
        expenses = storage.load_all_expenses()

        assert expenses == []

    def test_delete_expense(self, storage):
        """Test deleting expense file."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_to_delete")
        storage.save_expense(expense)

        result = storage.delete_expense("exp_to_delete")

        assert result is True
        expenses = storage.load_all_expenses()
        assert len(expenses) == 0

    def test_delete_nonexistent_expense(self, storage):
        """Test deleting expense that doesn't exist."""
        result = storage.delete_expense("nonexistent_id")

        assert result is False

    def test_get_expense_filename(self, storage):
        """Test filename generation."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_20251221_120000_abc123")

        filename = storage.get_expense_filename(expense)

        assert filename == "exp_20251221_120000_abc123.json"

    def test_get_all_expense_files(self, storage, temp_dir):
        """Test getting all expense files."""
        expense1 = Expense(50, "Food", "Lunch", expense_id="exp_1")
        expense2 = Expense(30, "Transport", "Taxi", expense_id="exp_2")
        storage.save_expense(expense1)
        storage.save_expense(expense2)

        with open(Path(temp_dir) / "not_an_expense.txt", 'w') as f:
            f.write("test")

        files = storage.get_all_expense_files()

        assert len(files) == 2
        filenames = [f.name for f in files]
        assert "exp_1.json" in filenames
        assert "exp_2.json" in filenames
        assert "not_an_expense.txt" not in filenames

    def test_invalid_json_handling(self, storage, temp_dir):
        """Test handling corrupted JSON files."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_valid")
        storage.save_expense(expense)

        corrupted_file = Path(temp_dir) / "exp_corrupted.json"
        with open(corrupted_file, 'w') as f:
            f.write("{invalid json")

        expenses = storage.load_all_expenses()

        assert len(expenses) == 1
        assert expenses[0].id == "exp_valid"

    def test_missing_fields_handling(self, storage, temp_dir):
        """Test handling JSON files with missing required fields."""
        expense = Expense(50, "Food", "Lunch", expense_id="exp_valid")
        storage.save_expense(expense)

        incomplete_file = Path(temp_dir) / "exp_incomplete.json"
        with open(incomplete_file, 'w') as f:
            json.dump({"id": "exp_incomplete"}, f)

        expenses = storage.load_all_expenses()

        assert len(expenses) == 1
        assert expenses[0].id == "exp_valid"

    def test_storage_persistence(self, temp_dir):
        """Test that data persists across storage instances."""
        storage1 = ExpenseStorage(temp_dir)
        expense = Expense(100, "Shopping", "Groceries", expense_id="exp_persist")
        storage1.save_expense(expense)

        storage2 = ExpenseStorage(temp_dir)
        expenses = storage2.load_all_expenses()

        assert len(expenses) == 1
        assert expenses[0].id == "exp_persist"
        assert expenses[0].amount == 100.0
