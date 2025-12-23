# Expense Tracker

A Python CLI application for tracking personal expenses with persistent file-based storage.

## Features

- **Add Expenses**: Track expenses with amount, category, description, and optional date
- **List All Expenses**: View all expenses sorted by creation time with running total
- **Category View**: Group and analyze expenses by category with subtotals
- **Delete Expenses**: Interactive deletion with confirmation prompts
- **File-Based Storage**: Each expense saved as a separate JSON file for portability
- **Input Validation**: Robust validation for amounts, categories, and dates
- **Auto-Generated IDs**: Unique identifiers for each expense
- **Error Handling**: Graceful handling of invalid data and corrupted files

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd expense-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the expense tracker:
```bash
python main.py
```

### Interactive Menu

The application provides an interactive menu with the following options:

1. **Add New Expense**
   - Enter amount (must be positive)
   - Specify category (e.g., Food, Transport, Entertainment)
   - Provide description
   - Optionally set date (defaults to today)
   - Auto-generates unique ID

2. **List All Expenses**
   - Displays all expenses in reverse chronological order
   - Shows date, category, amount, and description
   - Calculates and displays total amount
   - Shows count of expenses

3. **View Expenses by Category**
   - Groups expenses by category
   - Sorts categories alphabetically
   - Shows subtotal for each category
   - Displays grand total

4. **Delete Expense**
   - Lists all expenses with numbered index
   - Prompts for expense number to delete
   - Requires confirmation before deletion
   - Provides feedback on success/failure

5. **Exit**
   - Cleanly exits the application

### Example Workflow

```bash
$ python main.py

==================================================
           EXPENSE TRACKER
==================================================

1. Add New Expense
2. List All Expenses
3. View Expenses by Category
4. Delete Expense
5. Exit

==================================================

Enter your choice (1-5): 1

--- Add New Expense ---

Enter amount: $45.50
Enter category (e.g., Food, Transport, Entertainment): Food
Enter description: Grocery shopping
Enter date (YYYY-MM-DD, or press Enter for today):

✓ Expense added successfully!
  ID: exp_20251223_143022_a7b3c9
  2025-12-23 | Food            | $   45.50 | Grocery shopping
```

## Project Structure

```
expense-tracker/
├── main.py                           # Application entry point
├── data/                             # Expense JSON files storage
│   └── .gitkeep
├── src/                              # Source code
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── expense.py                # Expense data model
│   ├── storage/
│   │   ├── __init__.py
│   │   └── expense_storage.py        # File I/O operations
│   ├── ui/
│   │   ├── __init__.py
│   │   └── menu.py                   # Interactive CLI menu
│   └── utils/
│       ├── __init__.py
│       └── validators.py             # Input validation functions
├── tests/                            # Unit tests
│   ├── __init__.py
│   ├── test_expense.py
│   ├── test_expense_storage.py
│   ├── test_menu.py
│   └── test_validators.py
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Architecture

### Layered Design

The application follows a layered architecture pattern:

```
┌─────────────────────────────────────┐
│     Presentation Layer (UI)         │
│         menu.py                     │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    Application Logic Layer          │
│    expense.py + validators.py       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Data/Persistence Layer            │
│      expense_storage.py             │
└─────────────────────────────────────┘
```

### Key Components

#### 1. Expense Model (src/models/expense.py)
- Core data structure representing an expense
- Auto-generates unique IDs with format: `exp_YYYYMMDD_HHMMSS_<6char_hash>`
- Validates amount must be positive
- Provides serialization methods (to_dict/from_dict)
- Tracks creation timestamp and transaction date

#### 2. Storage Layer (src/storage/expense_storage.py)
- Manages file-based persistence
- Each expense stored as individual JSON file
- Handles file I/O operations (save, load, delete)
- Gracefully handles corrupted files with warnings
- Auto-creates data directory if missing

#### 3. UI Layer (src/ui/menu.py)
- Interactive command-line interface
- Menu-driven navigation
- Screen clearing for better user experience
- Real-time input validation
- Formatted output with alignment and totals

#### 4. Validation Utilities (src/utils/validators.py)
- Input validation and sanitization
- Amount validation (positive float)
- Category validation (non-empty, capitalized)
- Date validation (YYYY-MM-DD format)
- Retry logic for invalid input

## Data Storage

### File Format

Each expense is stored as a separate JSON file in the `data/` directory:

**Filename Format**: `exp_YYYYMMDD_HHMMSS_<hash>.json`

**File Contents**:
```json
{
  "id": "exp_20251223_143022_a7b3c9",
  "amount": 45.50,
  "category": "Food",
  "description": "Grocery shopping",
  "date": "2025-12-23",
  "created_at": "2025-12-23T14:30:22.123456"
}
```

### Storage Benefits

- **Human-Readable**: JSON format is easy to inspect and edit
- **Portable**: Files can be easily backed up or transferred
- **Simple**: No database setup required
- **Version Control**: Individual files work well with git
- **Fault Tolerant**: Corrupted files don't affect other expenses

## Testing

### Running Tests

Run all tests with pytest:
```bash
pytest tests/
```

Run with coverage report:
```bash
pytest tests/ --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_expense.py -v
```

### Test Coverage

The project includes comprehensive unit tests with 1.52:1 test-to-code ratio:

| Module | Test File | Test Count | Coverage Areas |
|--------|-----------|------------|----------------|
| Expense Model | test_expense.py | 10 | Creation, ID generation, validation, serialization |
| Storage Layer | test_expense_storage.py | 12 | Save, load, delete, error handling |
| UI Menu | test_menu.py | 19 | All menu options, user input, edge cases |
| Validators | test_validators.py | 13 | All validation functions, retry logic |

## Requirements

- Python 3.7+
- pytest 7.4.3 (for testing)
- pytest-cov 4.1.0 (for coverage reports)

## Error Handling

The application includes robust error handling:

- **Invalid Amount**: Must be a positive number
- **Empty Category**: Category cannot be blank
- **Invalid Date**: Must be YYYY-MM-DD format or empty
- **Corrupted Files**: Skipped with warning message
- **Keyboard Interrupt**: Graceful cancellation of operations
- **Missing Files**: Safe handling with appropriate messages

## Development

### Design Principles

- **Separation of Concerns**: Clear separation between UI, logic, and data layers
- **Single Responsibility**: Each module has one clear purpose
- **DRY (Don't Repeat Yourself)**: Reusable validation and storage functions
- **Error Handling**: Defensive programming with graceful degradation
- **Testability**: Modular design enables comprehensive unit testing

### Code Style

- Follows PEP 8 conventions
- Type hints in docstrings
- Comprehensive docstrings for all classes and functions
- Clear variable and function names
- Comments for complex logic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is available for educational purposes.

## Future Enhancements

Potential features for future development:

- **Export/Import**: CSV or Excel export functionality
- **Filtering**: Filter expenses by date range or amount
- **Search**: Search expenses by description or category
- **Budget Tracking**: Set and monitor category budgets
- **Reports**: Monthly/yearly expense reports with charts
- **Database Support**: Optional SQLite backend for larger datasets
- **Multi-Currency**: Support for different currencies with conversion
