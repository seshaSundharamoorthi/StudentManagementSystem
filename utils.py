"""
utils.py

This module contains validation utility functions and CLI input helper functions 
to validate student attributes and prompt users cleanly until valid input is received.
"""

import re
from typing import Callable, Any, Optional


def validate_name(name: str) -> bool:
    """
    Validates that a name contains only alphabetic characters and spaces,
    and is not empty.

    Args:
        name (str): The name to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    cleaned_name = name.strip()
    if not cleaned_name:
        return False
    # Check if the name consists of only letters and spaces
    return all(char.isalpha() or char.isspace() for char in cleaned_name)


def validate_age(age_str: str) -> bool:
    """
    Validates that the age is an integer between 15 and 100 inclusive.

    Args:
        age_str (str): The age input string.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        age = int(age_str.strip())
        return 15 <= age <= 100
    except ValueError:
        return False


def validate_gender(gender: str) -> bool:
    """
    Validates that gender is one of 'Male', 'Female', or 'Other' (case-insensitive).

    Args:
        gender (str): The gender string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    cleaned_gender = gender.strip().capitalize()
    return cleaned_gender in {"Male", "Female", "Other"}


def validate_year(year_str: str) -> bool:
    """
    Validates that the academic year is an integer between 1 and 5 inclusive.

    Args:
        year_str (str): The year input string.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        year = int(year_str.strip())
        return 1 <= year <= 5
    except ValueError:
        return False


def validate_email(email: str) -> bool:
    """
    Validates an email address using a standard regular expression.

    Args:
        email (str): The email string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    cleaned_email = email.strip()
    # RFC 5322 compliant simple email regex
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_regex, cleaned_email))


def validate_phone(phone: str) -> bool:
    """
    Validates that the phone number is exactly 10 digits.

    Args:
        phone (str): The phone number to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    cleaned_phone = phone.strip()
    return cleaned_phone.isdigit() and len(cleaned_phone) == 10


def get_validated_input(
    prompt: str,
    validation_func: Callable[[str], bool],
    error_msg: str,
    allow_empty: bool = False
) -> str:
    """
    Helper function to prompt the user for input and validate it.
    Repeats the prompt until a valid input is provided or (if allowed) an empty input is given.

    Args:
        prompt (str): The CLI input prompt message.
        validation_func (Callable[[str], bool]): The validation function to check input.
        error_msg (str): Error message to display when validation fails.
        allow_empty (bool): Whether to allow empty input (useful for optional updates).

    Returns:
        str: The validated input string.
    """
    while True:
        user_input = input(prompt).strip()
        if allow_empty and not user_input:
            return ""
        if validation_func(user_input):
            return user_input
        print(f"Error: {error_msg}")


# Specialized wrappers to keep prompt interface clean and uniform
def prompt_student_name(allow_empty: bool = False) -> str:
    """Prompts for student name with validation."""
    return get_validated_input(
        "Enter Name (Letters and spaces only): ",
        validate_name,
        "Name must contain only letters and spaces, and cannot be empty.",
        allow_empty
    )


def prompt_student_age(allow_empty: bool = False) -> int:
    """Prompts for student age with validation and returns int."""
    age_str = get_validated_input(
        "Enter Age (15-100): ",
        validate_age,
        "Age must be a valid integer between 15 and 100.",
        allow_empty
    )
    return int(age_str) if age_str else 0


def prompt_student_gender(allow_empty: bool = False) -> str:
    """Prompts for student gender with validation."""
    gender = get_validated_input(
        "Enter Gender (Male/Female/Other): ",
        validate_gender,
        "Gender must be either 'Male', 'Female', or 'Other'.",
        allow_empty
    )
    return gender.capitalize() if gender else ""


def prompt_student_department(allow_empty: bool = False) -> str:
    """Prompts for student department (cannot be empty if not updating)."""
    # Simple check: department shouldn't be empty if not updating
    def validate_dept(dept: str) -> bool:
        return len(dept.strip()) > 0

    return get_validated_input(
        "Enter Department: ",
        validate_dept,
        "Department cannot be empty.",
        allow_empty
    )


def prompt_student_year(allow_empty: bool = False) -> int:
    """Prompts for academic year with validation and returns int."""
    year_str = get_validated_input(
        "Enter Year (1-5): ",
        validate_year,
        "Year must be a valid integer between 1 and 5.",
        allow_empty
    )
    return int(year_str) if year_str else 0


def prompt_student_email(allow_empty: bool = False) -> str:
    """Prompts for student email with validation."""
    return get_validated_input(
        "Enter Email (e.g. name@domain.com): ",
        validate_email,
        "Please enter a valid email address.",
        allow_empty
    )


def prompt_student_phone(allow_empty: bool = False) -> str:
    """Prompts for student phone number with validation."""
    return get_validated_input(
        "Enter Phone Number (10 digits): ",
        validate_phone,
        "Phone number must be exactly 10 digits.",
        allow_empty
    )
