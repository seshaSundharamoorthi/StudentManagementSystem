"""
student.py

This module defines the Student class, representing individual student records 
within the Student Management System.
"""

from typing import Dict, Any


class Student:
    """
    Represents a student record with personal and academic details.
    """

    def __init__(
        self,
        student_id: str,
        name: str,
        age: int,
        gender: str,
        department: str,
        year: int,
        email: str,
        phone: str
    ) -> None:
        """
        Initializes a new Student instance.

        Args:
            student_id (str): The auto-generated unique identifier (e.g., STU1001).
            name (str): The full name of the student.
            age (int): The age of the student.
            gender (str): The gender of the student.
            department (str): The academic department.
            year (int): The current year of study (1-5).
            email (str): The email address of the student.
            phone (str): The contact phone number of the student.
        """
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.department = department
        self.year = year
        self.email = email
        self.phone = phone

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the student object properties into a dictionary.
        This is useful for JSON serialization.

        Returns:
            Dict[str, Any]: A dictionary representation of the student details.
        """
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "department": self.department,
            "year": self.year,
            "email": self.email,
            "phone": self.phone
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """
        Creates a Student instance from a dictionary.
        This is useful for deserializing loaded JSON data.

        Args:
            data (Dict[str, Any]): A dictionary containing student attributes.

        Returns:
            Student: An instantiated Student object.
        """
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            department=data["department"],
            year=data["year"],
            email=data["email"],
            phone=data["phone"]
        )

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the Student.

        Returns:
            str: Student info summary.
        """
        return f"Student ID: {self.student_id} | Name: {self.name} | Department: {self.department} | Year: {self.year}"
