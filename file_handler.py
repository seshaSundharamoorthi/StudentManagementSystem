"""
file_handler.py

This module contains the FileHandler class, which encapsulates all file-based
read and write operations for storing student records in JSON format.
"""

import json
import os
from typing import List, Dict, Any


class FileHandler:
    """
    Handles read/write operations on the persistent JSON storage file.
    Recovers gracefully if the file is missing or corrupted.
    """

    def __init__(self, filepath: str = "students.json") -> None:
        """
        Initializes the FileHandler with the target file path.

        Args:
            filepath (str): The file path where data is stored. Defaults to 'students.json'.
        """
        self.filepath = filepath

    def load_data(self) -> List[Dict[str, Any]]:
        """
        Reads student data from the JSON file. If the file is missing,
        empty, or corrupted, it automatically handles the error and 
        returns an empty list.

        Returns:
            List[Dict[str, Any]]: A list of student record dictionaries.
        """
        if not os.path.exists(self.filepath):
            # Create file with empty array if missing
            self.save_data([])
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                if isinstance(data, list):
                    return data
                return []
        except (json.JSONDecodeError, IOError, PermissionError) as e:
            # Handle corrupt file or read issues by backing up and resetting
            print(f"\n[Warning] Error reading storage file '{self.filepath}': {e}")
            print("[Warning] Re-initializing with an empty database.")
            # Automatically attempt to repair by saving empty database
            self.save_data([])
            return []

    def save_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        Saves student data to the JSON file in a human-readable formatted manner.

        Args:
            data (List[Dict[str, Any]]): The list of student dictionaries to save.

        Returns:
            bool: True if save operation succeeded, False otherwise.
        """
        try:
            # Ensure the directory exists if a nested path is specified
            dir_name = os.path.dirname(self.filepath)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)

            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except (IOError, TypeError, PermissionError) as e:
            print(f"\n[Error] Failed to write data to file '{self.filepath}': {e}")
            return False
