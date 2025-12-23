# Expense Tracker API Documentation

Complete API reference for all modules, classes, and functions in the Expense Tracker application.

## Table of Contents

1. [Models](#models)
   - [Expense](#expense)
2. [Storage](#storage)
   - [ExpenseStorage](#expensestorage)
3. [UI](#ui)
   - [ExpenseTrackerMenu](#expensetrackerмenu)
4. [Utils](#utils)
   - [Validators](#validators)

---

## Models

### Expense

**Module**: `src.models.expense`

**File**: `src/models/expense.py`

The `Expense` class represents a single expense transaction with automatic ID generation and validation.

#### Class: `Expense`

```python
class Expense:
    def __init__(self, amount, category, description, date=None, expense_id=None, created_at=None)
```

**Description**: Initialize an Expense instance with validation.

**Parameters**:
- `amount` (float): The expense amount (must be positive, > 0)
- `category` (str): The expense category (e.g., "Food", "Transport")
- `description` (str): Description of the expense
- `date` (str, optional): Date in ISO format (YYYY-MM-DD). Defaults to today if not provided
- `expense_id` (str, optional): Unique identifier. Auto-generated if not provided
- `created_at` (str, optional): Creation timestamp in ISO format. Auto-generated if not provided

**Raises**:
- `ValueError`: If amount is less than or equal to zero

**Attributes**:
- `amount` (float): The validated expense amount
- `category` (str): The expense category
- `description` (str): Expense description
- `date` (str): Transaction date in YYYY-MM-DD format
- `id` (str): Unique expense identifier (format: `exp_YYYYMMDD_HHMMSS_<6char_hash>`)
- `created_at` (str): ISO timestamp of when the expense was created

**Example**:
```python
from src.models.expense import Expense

# Create expense with default date
expense = Expense(
    amount=45.50,
    category="Food",
    description="Grocery shopping"
)

# Create expense with specific date
expense = Expense(
    amount=120.00,
    category="Transport",
    description="Monthly metro pass",
    date="2025-12-01"
)
```

---

#### Method: `generate_id()`

```python
@staticmethod
def generate_id() -> str
```

**Description**: Generate a unique expense ID using timestamp and random hash.

**Returns**:
- `str`: Unique expense ID in format `exp_YYYYMMDD_HHMMSS_<6char_hash>`

**Example**:
```python
expense_id = Expense.generate_id()
# Returns: "exp_20251223_143022_a7b3c9"
```

---

#### Method: `to_dict()`

```python
def to_dict(self) -> dict
```

**Description**: Convert expense to dictionary for JSON serialization.

**Returns**:
- `dict`: Dictionary representation with keys: `id`, `amount`, `category`, `description`, `date`, `created_at`

**Example**:
```python
expense = Expense(45.50, "Food", "Groceries")
data = expense.to_dict()
# Returns: {
#     "id": "exp_20251223_143022_a7b3c9",
#     "amount": 45.50,
#     "category": "Food",
#     "description": "Groceries",
#     "date": "2025-12-23",
#     "created_at": "2025-12-23T14:30:22.123456"
# }
```

---

#### Method: `from_dict()`

```python
@classmethod
def from_dict(cls, data: dict) -> Expense
```

**Description**: Create an Expense instance from a dictionary (deserialization).

**Parameters**:
- `data` (dict): Dictionary containing expense data with keys: `amount`, `category`, `description`, and optionally `date`, `id`, `created_at`

**Returns**:
- `Expense`: New Expense instance

**Example**:
```python
data = {
    "id": "exp_20251223_143022_a7b3c9",
    "amount": 45.50,
    "category": "Food",
    "description": "Groceries",
    "date": "2025-12-23",
    "created_at": "2025-12-23T14:30:22.123456"
}
expense = Expense.from_dict(data)
```

---

#### Method: `__str__()`

```python
def __str__(self) -> str
```

**Description**: String representation formatted for display.

**Returns**:
- `str`: Formatted string: `{date} | {category:15} | ${amount:8.2f} | {description}`

**Example**:
```python
expense = Expense(45.50, "Food", "Groceries", "2025-12-23")
print(expense)
# Outputs: "2025-12-23 | Food            | $   45.50 | Groceries"
```

---

## Storage

### ExpenseStorage

**Module**: `src.storage.expense_storage`

**File**: `src/storage/expense_storage.py`

The `ExpenseStorage` class handles file-based persistence for expenses, managing JSON file I/O operations.

#### Class: `ExpenseStorage`

```python
class ExpenseStorage:
    def __init__(self, data_dir="data")
```

**Description**: Initialize ExpenseStorage with data directory path.

**Parameters**:
- `data_dir` (str): Path to directory for storing expense JSON files. Defaults to "data"

**Attributes**:
- `data_dir` (Path): Path object pointing to the data directory

**Example**:
```python
from src.storage.expense_storage import ExpenseStorage

# Default data directory
storage = ExpenseStorage()

# Custom data directory
storage = ExpenseStorage("my_expenses")
```

---

#### Method: `ensure_data_directory()`

```python
def ensure_data_directory(self) -> None
```

**Description**: Create data directory if it doesn't exist. Called automatically during initialization.

**Returns**: None

---

#### Method: `save_expense()`

```python
def save_expense(self, expense: Expense) -> str
```

**Description**: Save a single expense to its own JSON file.

**Parameters**:
- `expense` (Expense): The expense object to save

**Returns**:
- `str`: Absolute path to the saved file

**File Naming**: Files are named using the expense ID: `{expense.id}.json`

**Example**:
```python
from src.models.expense import Expense
from src.storage.expense_storage import ExpenseStorage

storage = ExpenseStorage()
expense = Expense(45.50, "Food", "Groceries")
filepath = storage.save_expense(expense)
# Returns: "data/exp_20251223_143022_a7b3c9.json"
```

---

#### Method: `load_all_expenses()`

```python
def load_all_expenses(self) -> list[Expense]
```

**Description**: Load all expenses from JSON files in data directory with error handling for corrupted files.

**Returns**:
- `list[Expense]`: List of all successfully loaded Expense objects

**Error Handling**:
- Skips files with invalid JSON (JSONDecodeError)
- Skips files with missing required fields (KeyError)
- Skips files that fail Expense validation (ValueError)
- Prints warning message for each skipped file

**Example**:
```python
storage = ExpenseStorage()
expenses = storage.load_all_expenses()
for expense in expenses:
    print(expense)
```

---

#### Method: `delete_expense()`

```python
def delete_expense(self, expense_id: str) -> bool
```

**Description**: Delete an expense file by ID.

**Parameters**:
- `expense_id` (str): The unique ID of the expense to delete

**Returns**:
- `bool`: True if expense was found and deleted, False if not found

**Example**:
```python
storage = ExpenseStorage()
success = storage.delete_expense("exp_20251223_143022_a7b3c9")
if success:
    print("Expense deleted successfully")
else:
    print("Expense not found")
```

---

#### Method: `get_expense_filename()`

```python
def get_expense_filename(self, expense: Expense) -> str
```

**Description**: Generate filename for an expense based on its ID.

**Parameters**:
- `expense` (Expense): The expense object

**Returns**:
- `str`: Filename in format `{expense.id}.json`

**Example**:
```python
storage = ExpenseStorage()
expense = Expense(45.50, "Food", "Groceries")
filename = storage.get_expense_filename(expense)
# Returns: "exp_20251223_143022_a7b3c9.json"
```

---

#### Method: `get_all_expense_files()`

```python
def get_all_expense_files(self) -> list[Path]
```

**Description**: Get list of all expense JSON files in the data directory.

**Returns**:
- `list[Path]`: List of Path objects for files matching the expense file pattern

**Filtering**: Only returns files that:
- Have `.json` extension
- Start with `exp_` prefix

**Example**:
```python
storage = ExpenseStorage()
files = storage.get_all_expense_files()
for file in files:
    print(file.name)
```

---

## UI

### ExpenseTrackerMenu

**Module**: `src.ui.menu`

**File**: `src/ui/menu.py`

The `ExpenseTrackerMenu` class provides an interactive command-line interface for the expense tracker.

#### Class: `ExpenseTrackerMenu`

```python
class ExpenseTrackerMenu:
    def __init__(self, storage: ExpenseStorage)
```

**Description**: Initialize menu with storage instance.

**Parameters**:
- `storage` (ExpenseStorage): Storage instance for managing expenses

**Attributes**:
- `storage` (ExpenseStorage): The storage instance used for persistence

**Example**:
```python
from src.storage.expense_storage import ExpenseStorage
from src.ui.menu import ExpenseTrackerMenu

storage = ExpenseStorage()
menu = ExpenseTrackerMenu(storage)
menu.run()
```

---

#### Method: `run()`

```python
def run(self) -> None
```

**Description**: Main menu loop. Displays menu, processes user choices, and handles exit.

**Returns**: None

**Menu Options**:
1. Add New Expense
2. List All Expenses
3. View Expenses by Category
4. Delete Expense
5. Exit

**Flow**:
- Continuously displays menu until user selects Exit (5)
- Validates user choice (1-5)
- Calls appropriate method based on choice
- Prompts "Press Enter to continue" after operations
- Clears screen between operations

---

#### Method: `display_menu()`

```python
def display_menu(self) -> None
```

**Description**: Display formatted menu options with header and separator lines.

**Returns**: None

**Output Format**:
```
==================================================
           EXPENSE TRACKER
==================================================

1. Add New Expense
2. List All Expenses
3. View Expenses by Category
4. Delete Expense
5. Exit

==================================================
```

---

#### Method: `add_expense()`

```python
def add_expense(self) -> None
```

**Description**: Interactive prompt to add a new expense with validation.

**Returns**: None

**User Prompts**:
1. Amount (validated as positive float)
2. Category (validated as non-empty string)
3. Description (any text)
4. Date (optional, YYYY-MM-DD format)

**Success Output**:
- Confirmation message with checkmark
- Expense ID
- Formatted expense details

**Error Handling**:
- ValueError: Displays error message for invalid input
- KeyboardInterrupt: Cancels operation gracefully

**Example Session**:
```
--- Add New Expense ---

Enter amount: $45.50
Enter category (e.g., Food, Transport, Entertainment): Food
Enter description: Grocery shopping
Enter date (YYYY-MM-DD, or press Enter for today):

✓ Expense added successfully!
  ID: exp_20251223_143022_a7b3c9
  2025-12-23 | Food            | $   45.50 | Grocery shopping
```

---

#### Method: `list_expenses()`

```python
def list_expenses(self) -> None
```

**Description**: Display all expenses sorted by creation time (newest first) with total.

**Returns**: None

**Display Format**:
- Header row with column names
- Separator line
- Each expense on one line
- Total separator line
- Grand total and expense count

**Sorting**: Expenses sorted by `created_at` in descending order (newest first)

**Example Output**:
```
--- All Expenses ---

Date         | Category        |     Amount | Description
--------------------------------------------------------------------------------
2025-12-23 | Food            | $   45.50 | Grocery shopping
2025-12-22 | Transport       | $  120.00 | Monthly metro pass
2025-12-21 | Entertainment   | $   35.00 | Movie tickets
--------------------------------------------------------------------------------
             | TOTAL           | $  200.50 |

Total Expenses: 3
```

---

#### Method: `view_expenses_by_category()`

```python
def view_expenses_by_category(self) -> None
```

**Description**: Group and display expenses by category with subtotals and grand total.

**Returns**: None

**Grouping**: Expenses grouped by category, categories sorted alphabetically

**Display Format**:
- Category name as header
- Expenses within category sorted by date (newest first)
- Subtotal for each category
- Grand total at the end

**Example Output**:
```
--- Expenses by Category ---

Entertainment
--------------------------------------------------------------------------------
  2025-12-21   | $   35.00 | Movie tickets
  2025-12-15   | $   50.00 | Concert tickets
               | $   85.00 | Subtotal

Food
--------------------------------------------------------------------------------
  2025-12-23   | $   45.50 | Grocery shopping
  2025-12-20   | $   25.00 | Lunch
               | $   70.50 | Subtotal

Transport
--------------------------------------------------------------------------------
  2025-12-22   | $  120.00 | Monthly metro pass
               | $  120.00 | Subtotal

================================================================================
GRAND TOTAL: $275.50
```

---

#### Method: `delete_expense()`

```python
def delete_expense(self) -> None
```

**Description**: Interactive prompt to delete an expense with confirmation.

**Returns**: None

**Flow**:
1. Display numbered list of all expenses
2. Prompt user to select expense number
3. Allow cancellation (empty input)
4. Show expense details and ask for confirmation
5. Delete if confirmed, otherwise cancel

**Error Handling**:
- ValueError: Invalid number input
- KeyboardInterrupt: Cancels operation
- Index out of range: Invalid expense number

**Example Session**:
```
--- Delete Expense ---

  # | Date         | Category        |     Amount | Description
--------------------------------------------------------------------------------
  1 | 2025-12-23 | Food            | $   45.50 | Grocery shopping
  2 | 2025-12-22 | Transport       | $  120.00 | Monthly metro pass

Enter expense number to delete (or press Enter to cancel): 1
Delete 'Grocery shopping' ($45.50)? (y/N): y

✓ Expense deleted successfully!
```

---

#### Method: `get_user_choice()`

```python
def get_user_choice(self) -> str
```

**Description**: Get and return user's menu choice input.

**Returns**:
- `str`: User's input stripped of whitespace

**Note**: Validation of choice (1-5) is performed in the `run()` method

---

#### Method: `clear_screen()`

```python
def clear_screen(self) -> None
```

**Description**: Clear terminal screen for better user experience.

**Returns**: None

**Platform Support**:
- Unix/Linux/macOS: Uses `clear` command
- Windows: Uses `cls` command

---

## Utils

### Validators

**Module**: `src.utils.validators`

**File**: `src/utils/validators.py`

Validation functions for user input with error handling and retry logic.

---

#### Function: `validate_amount()`

```python
def validate_amount(amount_str: str) -> float
```

**Description**: Validate and convert amount string to positive float.

**Parameters**:
- `amount_str` (str): String representation of amount

**Returns**:
- `float`: Validated amount greater than zero

**Raises**:
- `ValueError`: If amount is not a valid number, is zero, or is negative

**Error Messages**:
- "Amount must be a valid number" - for non-numeric input
- "Amount must be greater than zero" - for zero or negative values

**Example**:
```python
from src.utils.validators import validate_amount

amount = validate_amount("45.50")  # Returns: 45.5
amount = validate_amount("0")       # Raises: ValueError("Amount must be greater than zero")
amount = validate_amount("abc")     # Raises: ValueError("Amount must be a valid number")
```

---

#### Function: `validate_category()`

```python
def validate_category(category: str) -> str
```

**Description**: Validate category input and capitalize first letter.

**Parameters**:
- `category` (str): Category string

**Returns**:
- `str`: Validated and capitalized category (first letter uppercase, rest lowercase)

**Raises**:
- `ValueError`: If category is empty after stripping whitespace

**Processing**:
1. Strips leading/trailing whitespace
2. Validates non-empty
3. Capitalizes first letter

**Example**:
```python
from src.utils.validators import validate_category

category = validate_category("food")         # Returns: "Food"
category = validate_category("  TRANSPORT")  # Returns: "Transport"
category = validate_category("")             # Raises: ValueError("Category cannot be empty")
category = validate_category("   ")          # Raises: ValueError("Category cannot be empty")
```

---

#### Function: `validate_date()`

```python
def validate_date(date_str: str) -> str
```

**Description**: Validate date format and return ISO format date string.

**Parameters**:
- `date_str` (str): Date string in YYYY-MM-DD format, or empty string

**Returns**:
- `str`: Validated date in YYYY-MM-DD format, or today's date if input is empty

**Raises**:
- `ValueError`: If date format is invalid

**Behavior**:
- Empty or whitespace-only input returns today's date
- Valid YYYY-MM-DD format returns the same date
- Invalid format raises ValueError

**Example**:
```python
from src.utils.validators import validate_date

date = validate_date("2025-12-23")    # Returns: "2025-12-23"
date = validate_date("")              # Returns: "2025-12-23" (today)
date = validate_date("   ")           # Returns: "2025-12-23" (today)
date = validate_date("12/23/2025")    # Raises: ValueError("Date must be in YYYY-MM-DD format")
date = validate_date("2025-13-01")    # Raises: ValueError("Date must be in YYYY-MM-DD format")
```

---

#### Function: `get_valid_input()`

```python
def get_valid_input(prompt: str, validator: callable = None) -> any
```

**Description**: Get and validate user input with retry logic for invalid input.

**Parameters**:
- `prompt` (str): Prompt message to display to user
- `validator` (callable, optional): Validation function to apply. If None, returns raw input

**Returns**:
- `any`: User input (type depends on validator return type), or raw string if no validator

**Retry Logic**:
- Continuously prompts user until valid input is provided
- Displays error message for invalid input
- Allows unlimited retry attempts

**Example**:
```python
from src.utils.validators import get_valid_input, validate_amount

# With validator
amount = get_valid_input("Enter amount: $", validate_amount)

# Without validator (returns raw string)
description = get_valid_input("Enter description: ")

# Interactive session with retry:
# Enter amount: $abc
# Invalid input: Amount must be a valid number
# Enter amount: $0
# Invalid input: Amount must be greater than zero
# Enter amount: $45.50
# (Returns 45.5)
```

---

## Error Handling

All modules include comprehensive error handling:

### Expense Model
- **ValueError**: Amount must be positive (> 0)

### Storage Layer
- **json.JSONDecodeError**: Skipped with warning (corrupted file)
- **KeyError**: Skipped with warning (missing required field)
- **ValueError**: Skipped with warning (invalid expense data)

### UI Layer
- **ValueError**: User-friendly error messages with retry
- **KeyboardInterrupt**: Graceful operation cancellation
- **IndexError**: Invalid selection handling

### Validators
- **ValueError**: Specific error messages for each validation type
- **TypeError**: Type conversion errors handled

---

## Usage Examples

### Complete Workflow Example

```python
from src.models.expense import Expense
from src.storage.expense_storage import ExpenseStorage
from src.ui.menu import ExpenseTrackerMenu

# Initialize storage
storage = ExpenseStorage("data")

# Create and save expenses
expense1 = Expense(45.50, "Food", "Grocery shopping", "2025-12-23")
expense2 = Expense(120.00, "Transport", "Monthly metro pass", "2025-12-22")

storage.save_expense(expense1)
storage.save_expense(expense2)

# Load all expenses
expenses = storage.load_all_expenses()
for expense in expenses:
    print(expense)

# Delete an expense
storage.delete_expense(expense1.id)

# Run interactive menu
menu = ExpenseTrackerMenu(storage)
menu.run()
```

### Programmatic Expense Management

```python
from src.models.expense import Expense
from src.storage.expense_storage import ExpenseStorage

# Initialize storage
storage = ExpenseStorage()

# Add multiple expenses
expenses_data = [
    (45.50, "Food", "Groceries"),
    (120.00, "Transport", "Metro pass"),
    (35.00, "Entertainment", "Movie tickets")
]

for amount, category, description in expenses_data:
    expense = Expense(amount, category, description)
    storage.save_expense(expense)

# Load and analyze
all_expenses = storage.load_all_expenses()

# Calculate total by category
categories = {}
for expense in all_expenses:
    if expense.category not in categories:
        categories[expense.category] = 0
    categories[expense.category] += expense.amount

# Print summary
for category, total in sorted(categories.items()):
    print(f"{category}: ${total:.2f}")
```

---

## Type Reference

### Expense Dictionary Format

```python
{
    "id": str,              # Format: "exp_YYYYMMDD_HHMMSS_<hash>"
    "amount": float,        # Positive number
    "category": str,        # Capitalized string
    "description": str,     # Any string
    "date": str,            # Format: "YYYY-MM-DD"
    "created_at": str       # ISO format: "YYYY-MM-DDTHH:MM:SS.ffffff"
}
```

### File Naming Convention

- **Pattern**: `exp_YYYYMMDD_HHMMSS_<6char_hash>.json`
- **Example**: `exp_20251223_143022_a7b3c9.json`
- **Location**: `data/` directory

---

## Version Information

- **Python Version**: 3.7+
- **Dependencies**: None for core functionality (pytest for testing)
- **File Format**: JSON (RFC 8259)
- **Date Format**: ISO 8601 (YYYY-MM-DD)
- **Timestamp Format**: ISO 8601 with microseconds
