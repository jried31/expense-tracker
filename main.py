#!/usr/bin/env python3
"""
Expense Tracker - Main Entry Point

A CLI application for tracking personal expenses.
"""
from src.storage.expense_storage import ExpenseStorage
from src.ui.menu import ExpenseTrackerMenu


def main():
    """Main entry point for the expense tracker application."""
    try:
        storage = ExpenseStorage("data")
        menu = ExpenseTrackerMenu(storage)
        menu.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
