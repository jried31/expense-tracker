# Developer Guide

Complete guide for developers who want to understand, modify, or extend the Expense Tracker application.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Architecture](#project-architecture)
3. [Code Organization](#code-organization)
4. [Development Workflow](#development-workflow)
5. [Testing Strategy](#testing-strategy)
6. [Adding New Features](#adding-new-features)
7. [Code Style Guide](#code-style-guide)
8. [Common Tasks](#common-tasks)
9. [Troubleshooting](#troubleshooting)

---

## Development Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (for version control)

### Initial Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd expense-tracker
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run tests to verify setup:
```bash
pytest tests/ -v
```

### Development Dependencies

The project uses minimal dependencies:
- **pytest** (7.4.3): Testing framework
- **pytest-cov** (4.1.0): Test coverage reporting

No runtime dependencies - the application uses only Python standard library.

---

## Project Architecture

### Layered Architecture

The application follows a clean layered architecture pattern:

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                      │
│                                                          │
│  ExpenseTrackerMenu (src/ui/menu.py)                    │
│  - User interaction                                      │
│  - Input/output formatting                              │
│  - Screen management                                     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                Application Logic Layer                   │
│                                                          │
│  Expense Model (src/models/expense.py)                  │
│  - Data validation                                       │
│  - Business logic                                        │
│  - ID generation                                         │
│                                                          │
│  Validators (src/utils/validators.py)                   │
│  - Input validation                                      │
│  - Data sanitization                                     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                Data/Persistence Layer                    │
│                                                          │
│  ExpenseStorage (src/storage/expense_storage.py)        │
│  - File I/O operations                                   │
│  - Data serialization                                    │
│  - Error handling for corrupted data                    │
└─────────────────────────────────────────────────────────┘
```

### Design Patterns

1. **Repository Pattern**: `ExpenseStorage` acts as a repository, abstracting data access
2. **Facade Pattern**: `ExpenseTrackerMenu` provides a simplified interface to the system
3. **Factory Pattern**: `Expense.from_dict()` creates objects from data
4. **Validator Pattern**: Dedicated validation functions in `validators.py`

### Key Design Principles

- **Separation of Concerns**: Each layer has a single, well-defined responsibility
- **Single Responsibility**: Each class/module does one thing well
- **Open/Closed Principle**: Easy to extend without modifying existing code
- **Dependency Inversion**: Higher layers depend on abstractions, not concrete implementations
- **DRY (Don't Repeat Yourself)**: Common functionality is extracted into reusable functions

---

## Code Organization

### Directory Structure

```
expense-tracker/
├── main.py                        # Application entry point
├── requirements.txt               # Python dependencies
├── README.md                      # User documentation
│
├── src/                          # Source code
│   ├── __init__.py
│   │
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   └── expense.py           # Expense class
│   │
│   ├── storage/                 # Persistence layer
│   │   ├── __init__.py
│   │   └── expense_storage.py  # File I/O operations
│   │
│   ├── ui/                      # User interface
│   │   ├── __init__.py
│   │   └── menu.py             # CLI menu system
│   │
│   └── utils/                   # Utilities
│       ├── __init__.py
│       └── validators.py       # Input validation
│
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_expense.py
│   ├── test_expense_storage.py
│   ├── test_menu.py
│   └── test_validators.py
│
├── data/                        # Expense data files
│   └── .gitkeep
│
└── docs/                        # Documentation
    ├── API.md
    ├── COVERAGE.md
    └── DEVELOPER_GUIDE.md
```

### Module Responsibilities

#### src/models/expense.py
- Defines the `Expense` data model
- Validates expense data (amount must be positive)
- Generates unique IDs
- Handles serialization/deserialization

#### src/storage/expense_storage.py
- Manages file-based persistence
- Saves/loads/deletes expense files
- Handles file system operations
- Manages corrupted file recovery

#### src/ui/menu.py
- Provides interactive CLI interface
- Handles user input
- Formats output display
- Manages screen clearing

#### src/utils/validators.py
- Validates user input
- Sanitizes data
- Provides retry logic for invalid input

---

## Development Workflow

### Making Changes

1. **Create a feature branch**:
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**:
   - Edit code
   - Update docstrings
   - Add/update tests

3. **Run tests**:
```bash
pytest tests/ -v
```

4. **Check test coverage**:
```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html  # View coverage report
```

5. **Commit changes**:
```bash
git add .
git commit -m "Add feature: description"
```

6. **Push and create PR**:
```bash
git push origin feature/your-feature-name
```

### Code Review Checklist

Before submitting a PR, ensure:

- ✓ All tests pass
- ✓ Test coverage remains high (>90%)
- ✓ New features have tests
- ✓ Docstrings updated
- ✓ Code follows style guide
- ✓ No new dependencies added (unless necessary)
- ✓ README updated if needed
- ✓ API documentation updated if needed

---

## Testing Strategy

### Test Organization

The test suite mirrors the source structure:

```
src/models/expense.py      → tests/test_expense.py
src/storage/expense_storage.py → tests/test_expense_storage.py
src/ui/menu.py            → tests/test_menu.py
src/utils/validators.py   → tests/test_validators.py
```

### Testing Approach

1. **Unit Tests**: Test individual functions/methods in isolation
2. **Mocking**: Use mocks for I/O operations (files, user input)
3. **Fixtures**: Use pytest fixtures for common test setup
4. **Edge Cases**: Test boundary conditions and error cases

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_expense.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src

# Run with HTML coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_expense.py::test_expense_creation_with_valid_data -v
```

### Writing Tests

#### Test Naming Convention
```python
def test_<component>_<scenario>():
    """Test description."""
```

#### Example Test Structure
```python
import pytest
from src.models.expense import Expense

def test_expense_creation_with_valid_data():
    """Test that expense is created successfully with valid data."""
    # Arrange
    amount = 45.50
    category = "Food"
    description = "Groceries"

    # Act
    expense = Expense(amount, category, description)

    # Assert
    assert expense.amount == amount
    assert expense.category == category
    assert expense.description == description

def test_expense_creation_with_invalid_amount():
    """Test that expense creation fails with invalid amount."""
    # Arrange
    amount = -10.00
    category = "Food"
    description = "Groceries"

    # Act & Assert
    with pytest.raises(ValueError, match="Amount must be greater than zero"):
        Expense(amount, category, description)
```

### Test Fixtures

Use fixtures for common setup:

```python
import pytest
import tempfile
from pathlib import Path
from src.storage.expense_storage import ExpenseStorage

@pytest.fixture
def temp_storage():
    """Fixture providing temporary storage directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield ExpenseStorage(tmpdir)
```

---

## Adding New Features

### Example: Adding a Search Feature

Follow these steps to add a new feature:

#### 1. Plan the Feature

**Requirement**: Search expenses by description keyword

**Impact Analysis**:
- New method in `ExpenseStorage`: `search_expenses(keyword)`
- New menu option in `ExpenseTrackerMenu`: "Search Expenses"
- No changes to `Expense` model needed
- No new validation needed

#### 2. Write Tests First (TDD)

**tests/test_expense_storage.py**:
```python
def test_search_expenses_finds_matching_expenses(temp_storage):
    """Test search finds expenses matching keyword."""
    # Arrange
    expense1 = Expense(50.00, "Food", "Grocery shopping")
    expense2 = Expense(30.00, "Food", "Restaurant dinner")
    expense3 = Expense(100.00, "Transport", "Taxi ride")

    temp_storage.save_expense(expense1)
    temp_storage.save_expense(expense2)
    temp_storage.save_expense(expense3)

    # Act
    results = temp_storage.search_expenses("shopping")

    # Assert
    assert len(results) == 1
    assert results[0].description == "Grocery shopping"

def test_search_expenses_is_case_insensitive(temp_storage):
    """Test search is case-insensitive."""
    # Arrange
    expense = Expense(50.00, "Food", "Grocery Shopping")
    temp_storage.save_expense(expense)

    # Act
    results = temp_storage.search_expenses("grocery")

    # Assert
    assert len(results) == 1

def test_search_expenses_returns_empty_list_when_no_matches(temp_storage):
    """Test search returns empty list when no matches found."""
    # Arrange
    expense = Expense(50.00, "Food", "Groceries")
    temp_storage.save_expense(expense)

    # Act
    results = temp_storage.search_expenses("restaurant")

    # Assert
    assert len(results) == 0
```

#### 3. Implement the Feature

**src/storage/expense_storage.py**:
```python
def search_expenses(self, keyword):
    """
    Search expenses by description keyword.

    Args:
        keyword (str): Search keyword (case-insensitive)

    Returns:
        list[Expense]: List of expenses matching the keyword
    """
    all_expenses = self.load_all_expenses()
    keyword_lower = keyword.lower()

    return [
        expense for expense in all_expenses
        if keyword_lower in expense.description.lower()
    ]
```

#### 4. Add UI Integration

**src/ui/menu.py**:
```python
def display_menu(self):
    """Display menu options."""
    self.clear_screen()
    print("=" * 50)
    print("           EXPENSE TRACKER")
    print("=" * 50)
    print("\n1. Add New Expense")
    print("2. List All Expenses")
    print("3. View Expenses by Category")
    print("4. Search Expenses")  # New option
    print("5. Delete Expense")
    print("6. Exit")  # Updated number
    print("\n" + "=" * 50)

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
            self.search_expenses()  # New handler
        elif choice == '5':
            self.delete_expense()
        elif choice == '6':
            print("\nThank you for using Expense Tracker. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1-6.")

        if choice in ['1', '2', '3', '4', '5']:
            input("\nPress Enter to continue...")

def search_expenses(self):
    """Interactive search for expenses."""
    print("\n--- Search Expenses ---\n")

    keyword = input("Enter search keyword: ").strip()

    if not keyword:
        print("Search cancelled.")
        return

    results = self.storage.search_expenses(keyword)

    if not results:
        print(f"\nNo expenses found matching '{keyword}'.")
        return

    print(f"\nFound {len(results)} expense(s) matching '{keyword}':\n")
    print(f"{'Date':12} | {'Category':15} | {'Amount':>10} | Description")
    print("-" * 80)

    total = 0
    for expense in sorted(results, key=lambda e: e.date, reverse=True):
        print(expense)
        total += expense.amount

    print("-" * 80)
    print(f"{'':12} | {'TOTAL':15} | ${total:>9.2f} |")
```

#### 5. Add Tests for UI

**tests/test_menu.py**:
```python
def test_search_expenses_displays_results(mock_storage, capsys):
    """Test search displays matching expenses."""
    # Setup mock
    expense = Expense(50.00, "Food", "Grocery shopping")
    mock_storage.search_expenses.return_value = [expense]

    menu = ExpenseTrackerMenu(mock_storage)

    # Mock user input
    with patch('builtins.input', side_effect=["grocery"]):
        menu.search_expenses()

    # Verify
    mock_storage.search_expenses.assert_called_once_with("grocery")
    captured = capsys.readouterr()
    assert "Grocery shopping" in captured.out
    assert "Found 1 expense(s)" in captured.out
```

#### 6. Update Documentation

- Update README.md with new menu option
- Update docs/API.md with new method documentation
- Update in-code docstrings

#### 7. Run All Tests

```bash
pytest tests/ -v
pytest tests/ --cov=src
```

#### 8. Commit Changes

```bash
git add .
git commit -m "Add expense search functionality

- Add search_expenses() method to ExpenseStorage
- Add search menu option to ExpenseTrackerMenu
- Add comprehensive tests for search functionality
- Update documentation"
```

---

## Code Style Guide

### Python Style

Follow PEP 8 conventions:

```python
# Good: Clear naming, proper spacing
def validate_amount(amount_str):
    """Validate and convert amount to float."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        return amount
    except (ValueError, TypeError) as e:
        raise ValueError("Amount must be a valid number")

# Bad: Unclear naming, poor spacing
def val_amt(a):
    try:
        x=float(a)
        if x<=0:raise ValueError("bad")
        return x
    except:
        raise ValueError("bad")
```

### Naming Conventions

- **Classes**: PascalCase (`Expense`, `ExpenseStorage`)
- **Functions/Methods**: snake_case (`validate_amount`, `save_expense`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_AMOUNT`, `DEFAULT_CATEGORY`)
- **Private methods**: Leading underscore (`_internal_method`)

### Docstring Format

Use Google-style docstrings:

```python
def method_name(param1, param2):
    """
    Brief description of what the method does.

    Longer description if needed, explaining the behavior,
    side effects, or important notes.

    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2

    Returns:
        type: Description of return value

    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### Error Handling

```python
# Good: Specific exceptions, clear messages
try:
    amount = float(amount_str)
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
except ValueError:
    raise ValueError("Amount must be a valid number")

# Bad: Bare except, unclear error
try:
    amount = float(amount_str)
    if amount <= 0:
        raise Exception("Bad amount")
except:
    raise Exception("Error")
```

### Import Organization

```python
# Standard library imports
import json
import os
from datetime import datetime
from pathlib import Path

# Third-party imports
import pytest

# Local imports
from src.models.expense import Expense
from src.storage.expense_storage import ExpenseStorage
```

---

## Common Tasks

### Adding a New Validation Rule

**File**: `src/utils/validators.py`

```python
def validate_email(email):
    """
    Validate email format.

    Args:
        email (str): Email address

    Returns:
        str: Validated email in lowercase

    Raises:
        ValueError: If email format is invalid
    """
    import re
    email = email.strip().lower()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(pattern, email):
        raise ValueError("Email must be in format: user@example.com")

    return email
```

### Adding a New Menu Option

See [Adding New Features](#adding-new-features) section for complete example.

### Changing Data Storage Format

To migrate from JSON to a different format:

1. Create new storage class implementing same interface
2. Add migration script
3. Update initialization in main.py
4. Add tests for new storage format
5. Update documentation

### Adding a New Expense Field

Example: Adding "payment_method" field

1. Update `Expense.__init__()` to accept new parameter
2. Update `Expense.to_dict()` to include new field
3. Update `Expense.from_dict()` to handle new field
4. Update all test fixtures
5. Add validation if needed
6. Update UI to prompt for new field
7. Update documentation

---

## Troubleshooting

### Common Issues

#### Issue: Tests Fail After Changes

**Solution**:
1. Check if test data needs updating
2. Verify mock objects match new signatures
3. Run tests with `-v` flag for details
4. Check test fixtures are up to date

#### Issue: Import Errors

**Solution**:
1. Verify virtual environment is activated
2. Ensure all `__init__.py` files exist
3. Check PYTHONPATH includes project root
4. Reinstall dependencies: `pip install -r requirements.txt`

#### Issue: File Permission Errors

**Solution**:
1. Check data directory permissions
2. Verify user has write access
3. Try different data directory
4. Check disk space

#### Issue: JSON Decode Errors

**Solution**:
1. Check for corrupted JSON files in data/
2. Validate JSON format
3. Delete corrupted files or fix manually
4. Application handles this gracefully with warnings

### Debugging Tips

```python
# Add debug prints
import json
print(f"DEBUG: expense = {json.dumps(expense.to_dict(), indent=2)}")

# Use breakpoint()
def problematic_function():
    breakpoint()  # Drops into debugger
    # code continues

# Run with pytest verbose
pytest tests/test_expense.py::test_name -v -s

# Use pytest fixtures to inspect state
@pytest.fixture
def debug_storage(temp_storage):
    yield temp_storage
    # Inspect state after test
    print(f"Files: {list(temp_storage.get_all_expense_files())}")
```

---

## Performance Considerations

### Current Performance

- **Load Time**: O(n) where n = number of expense files
- **Save Time**: O(1) - single file write
- **Delete Time**: O(n) - must search all files for ID
- **Search Time**: O(n) - must load all expenses

### Optimization Opportunities

For large datasets (>10,000 expenses):

1. **Add Index File**: Maintain index of all expenses
2. **Use Database**: Migrate to SQLite for better performance
3. **Lazy Loading**: Load expenses on-demand
4. **Caching**: Cache frequently accessed data
5. **Batch Operations**: Support bulk import/export

### Current Limits

With file-based storage:
- Recommended max: ~10,000 expenses
- Load time: ~1-2 seconds for 10,000 files
- Disk space: ~500 bytes per expense

---

## Security Considerations

### Current Security

- **No Authentication**: Single-user application
- **Local Storage**: Files stored locally, not transmitted
- **No Encryption**: JSON files are plain text
- **Input Validation**: Prevents injection attacks

### Security Best Practices

If extending the application:

1. **Never store sensitive data** (SSN, credit cards) in plain text
2. **Validate all input** before processing
3. **Sanitize file paths** to prevent directory traversal
4. **Use parameterized queries** if adding database
5. **Encrypt sensitive data** at rest if needed

---

## Future Development

### Planned Features

See README.md "Future Enhancements" section for:
- Export/Import functionality
- Filtering capabilities
- Budget tracking
- Reporting features
- Database support

### Extension Points

The architecture supports easy extension:

1. **New Storage Backend**: Implement storage interface
2. **New UI**: Replace menu.py with GUI/web interface
3. **New Validators**: Add to validators.py
4. **New Reports**: Add methods to menu or storage
5. **Plugins**: Create plugin system for custom features

---

## Resources

### Documentation
- [README.md](../README.md): User documentation
- [API.md](API.md): Complete API reference
- [COVERAGE.md](COVERAGE.md): Documentation coverage report

### Python Resources
- [PEP 8](https://pep8.org/): Style Guide
- [pytest Documentation](https://docs.pytest.org/): Testing framework
- [Python Documentation](https://docs.python.org/3/): Standard library

### Tools
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **git**: Version control

---

## Contact & Contributing

For questions, issues, or contributions:

1. Check existing documentation
2. Review test cases for examples
3. Create an issue for bugs
4. Submit a PR for features

Follow the [Code Review Checklist](#code-review-checklist) for all PRs.
