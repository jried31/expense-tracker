# Expense Tracker

A Python CLI application for tracking personal expenses.

## Features

- Add expenses with amount, category, and description
- List all expenses with total
- View expenses grouped by category
- Delete expenses
- Each expense saved as a separate JSON file

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

Follow the interactive menu to:
1. Add New Expense
2. List All Expenses
3. View Expenses by Category
4. Delete Expense
5. Exit

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Project Structure

```
expense-tracker/
├── main.py                    # Application entry point
├── data/                      # Expense JSON files
├── src/                       # Source code
│   ├── models/               # Data models
│   ├── storage/              # File I/O operations
│   ├── ui/                   # User interface
│   └── utils/                # Validation utilities
└── tests/                    # Unit tests
```
