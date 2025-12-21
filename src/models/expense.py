from datetime import datetime
import random
import string


class Expense:
    def __init__(self, amount, category, description, date=None, expense_id=None, created_at=None):
        """
        Initialize an Expense instance.

        Args:
            amount (float): The expense amount (must be positive)
            category (str): The expense category
            description (str): Description of the expense
            date (str, optional): Date in ISO format (YYYY-MM-DD). Defaults to today.
            expense_id (str, optional): Unique identifier. Auto-generated if not provided.
            created_at (str, optional): Creation timestamp. Auto-generated if not provided.
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.id = expense_id if expense_id else self.generate_id()
        self.created_at = created_at if created_at else datetime.now().isoformat()

    @staticmethod
    def generate_id():
        """
        Generate a unique expense ID.

        Format: exp_YYYYMMDD_HHMMSS_<6char_hash>

        Returns:
            str: Unique expense ID
        """
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        random_hash = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"exp_{timestamp}_{random_hash}"

    def to_dict(self):
        """
        Convert expense to dictionary for JSON serialization.

        Returns:
            dict: Dictionary representation of the expense
        """
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an Expense instance from a dictionary.

        Args:
            data (dict): Dictionary containing expense data

        Returns:
            Expense: New Expense instance
        """
        return cls(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data.get("date"),
            expense_id=data.get("id"),
            created_at=data.get("created_at")
        )

    def __str__(self):
        """
        String representation for display.

        Returns:
            str: Formatted expense string
        """
        return f"{self.date} | {self.category:15} | ${self.amount:8.2f} | {self.description}"
