import json
import os
from pathlib import Path
from src.models.expense import Expense


class ExpenseStorage:
    def __init__(self, data_dir="data"):
        """
        Initialize ExpenseStorage with data directory path.

        Args:
            data_dir (str): Path to directory for storing expense JSON files
        """
        self.data_dir = Path(data_dir)
        self.ensure_data_directory()

    def ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_expense(self, expense):
        """
        Save a single expense to its own JSON file.

        Args:
            expense (Expense): The expense to save

        Returns:
            str: Path to the saved file
        """

        filename = self.get_expense_filename(expense)
        filepath = self.data_dir / filename

        with open(filepath, 'w') as f:
            json.dump(expense.to_dict(), f, indent=2)

        return str(filepath)

    def load_all_expenses(self):
        """
        Load all expenses from JSON files in data directory.

        Returns:
            list[Expense]: List of all Expense objects
        """
        expenses = []

        for filepath in self.get_all_expense_files():
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    expenses.append(Expense.from_dict(data))
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: Could not load {filepath.name}: {e}")
                continue

        return expenses

    def delete_expense(self, expense_id):
        """
        Delete an expense file by ID.

        Args:
            expense_id (str): The ID of the expense to delete

        Returns:
            bool: True if deleted, False if not found
        """
        for filepath in self.get_all_expense_files():
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if data.get("id") == expense_id:
                        filepath.unlink()
                        return True
            except (json.JSONDecodeError, KeyError):
                continue

        return False

    def get_expense_filename(self, expense):
        """
        Generate filename for an expense.

        Format: exp_YYYYMMDD_HHMMSS_<hash>.json

        Args:
            expense (Expense): The expense object

        Returns:
            str: Filename for the expense
        """
        return f"{expense.id}.json"

    def get_all_expense_files(self):
        """
        Get list of all expense JSON files.

        Returns:
            list[Path]: List of Path objects for expense files
        """
        if not self.data_dir.exists():
            return []

        return [f for f in self.data_dir.iterdir() if f.suffix == '.json' and f.name.startswith('exp_')]
