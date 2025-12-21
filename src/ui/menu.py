import os
from src.models.expense import Expense
from src.utils.validators import validate_amount, validate_category, validate_date, get_valid_input


class ExpenseTrackerMenu:
    def __init__(self, storage):
        """
        Initialize menu with storage instance.

        Args:
            storage (ExpenseStorage): Storage instance for managing expenses
        """
        self.storage = storage

    def run(self):
        """Main menu loop."""
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.list_expenses()
            elif choice == '3':
                self.view_expenses_by_category()
            elif choice == '4':
                self.delete_expense()
            elif choice == '5':
                print("\nThank you for using Expense Tracker. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please select 1-5.")

            if choice in ['1', '2', '3', '4']:
                input("\nPress Enter to continue...")

    def display_menu(self):
        """Display menu options."""
        self.clear_screen()
        print("=" * 50)
        print("           EXPENSE TRACKER")
        print("=" * 50)
        print("\n1. Add New Expense")
        print("2. List All Expenses")
        print("3. View Expenses by Category")
        print("4. Delete Expense")
        print("5. Exit")
        print("\n" + "=" * 50)

    def add_expense(self):
        """Interactive prompt to add new expense."""
        print("\n--- Add New Expense ---\n")

        try:
            amount = get_valid_input("Enter amount: $", validate_amount)
            category = get_valid_input("Enter category (e.g., Food, Transport, Entertainment): ", validate_category)
            description = input("Enter description: ").strip()
            date_input = input("Enter date (YYYY-MM-DD, or press Enter for today): ").strip()
            date = validate_date(date_input)

            expense = Expense(amount, category, description, date)
            self.storage.save_expense(expense)

            print("\n✓ Expense added successfully!")
            print(f"  ID: {expense.id}")
            print(f"  {expense}")

        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")

    def list_expenses(self):
        """Display all expenses with total."""
        print("\n--- All Expenses ---\n")

        expenses = self.storage.load_all_expenses()

        if not expenses:
            print("No expenses found.")
            return

        expenses.sort(key=lambda e: e.created_at, reverse=True)

        print(f"{'Date':12} | {'Category':15} | {'Amount':>10} | Description")
        print("-" * 80)

        total = 0
        for expense in expenses:
            print(expense)
            total += expense.amount

        print("-" * 80)
        print(f"{'':12} | {'TOTAL':15} | ${total:>9.2f} |")
        print(f"\nTotal Expenses: {len(expenses)}")

    def view_expenses_by_category(self):
        """Group and display expenses by category."""
        print("\n--- Expenses by Category ---\n")

        expenses = self.storage.load_all_expenses()

        if not expenses:
            print("No expenses found.")
            return

        categories = {}
        for expense in expenses:
            if expense.category not in categories:
                categories[expense.category] = []
            categories[expense.category].append(expense)

        grand_total = 0
        for category, category_expenses in sorted(categories.items()):
            category_total = sum(e.amount for e in category_expenses)
            grand_total += category_total

            print(f"\n{category}")
            print("-" * 80)
            for expense in sorted(category_expenses, key=lambda e: e.date, reverse=True):
                print(f"  {expense.date:12} | ${expense.amount:8.2f} | {expense.description}")
            print(f"  {'':12} | ${category_total:8.2f} | Subtotal")

        print("\n" + "=" * 80)
        print(f"GRAND TOTAL: ${grand_total:.2f}")

    def delete_expense(self):
        """Interactive prompt to delete expense."""
        print("\n--- Delete Expense ---\n")

        expenses = self.storage.load_all_expenses()

        if not expenses:
            print("No expenses found.")
            return

        expenses.sort(key=lambda e: e.created_at, reverse=True)

        print(f"{'#':3} | {'Date':12} | {'Category':15} | {'Amount':>10} | Description")
        print("-" * 80)

        for idx, expense in enumerate(expenses, 1):
            print(f"{idx:3} | {expense}")

        print()
        try:
            choice = input("Enter expense number to delete (or press Enter to cancel): ").strip()

            if not choice:
                print("Deletion cancelled.")
                return

            idx = int(choice) - 1
            if 0 <= idx < len(expenses):
                expense = expenses[idx]
                confirm = input(f"Delete '{expense.description}' (${expense.amount:.2f})? (y/N): ").strip().lower()

                if confirm == 'y':
                    if self.storage.delete_expense(expense.id):
                        print("\n✓ Expense deleted successfully!")
                    else:
                        print("\n✗ Error: Could not delete expense.")
                else:
                    print("\nDeletion cancelled.")
            else:
                print("\n✗ Invalid expense number.")

        except ValueError:
            print("\n✗ Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")

    def get_user_choice(self):
        """
        Get and validate menu choice.

        Returns:
            str: User's menu choice
        """
        return input("\nEnter your choice (1-5): ").strip()

    def clear_screen(self):
        """Clear terminal screen for better UX."""
        os.system('clear' if os.name != 'nt' else 'cls')
