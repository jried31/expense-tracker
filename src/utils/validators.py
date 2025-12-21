from datetime import datetime


def validate_amount(amount_str):
    """
    Validate and convert amount to float.

    Args:
        amount_str (str): String representation of amount

    Returns:
        float: Validated amount

    Raises:
        ValueError: If amount is invalid (negative, zero, or not a number)
    """
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        return amount
    except (ValueError, TypeError) as e:
        if "could not convert" in str(e) or "invalid literal" in str(e):
            raise ValueError("Amount must be a valid number")
        raise


def validate_category(category):
    """
    Validate category input.

    Args:
        category (str): Category string

    Returns:
        str: Validated and capitalized category

    Raises:
        ValueError: If category is empty
    """
    category = category.strip()
    if not category:
        raise ValueError("Category cannot be empty")
    return category.capitalize()


def validate_date(date_str):
    """
    Validate date format.

    Args:
        date_str (str): Date string in ISO format (YYYY-MM-DD) or empty

    Returns:
        str: Validated date in ISO format

    Raises:
        ValueError: If date format is invalid
    """
    if not date_str or date_str.strip() == "":
        return datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")


def get_valid_input(prompt, validator=None):
    """
    Get and validate user input.

    Args:
        prompt (str): Prompt to display to user
        validator (callable, optional): Validation function to apply

    Returns:
        str or validated type: User input, optionally validated
    """
    while True:
        user_input = input(prompt)
        if validator is None:
            return user_input

        try:
            return validator(user_input)
        except ValueError as e:
            print(f"Invalid input: {e}")
