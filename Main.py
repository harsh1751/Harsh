#!/usr/bin/env python3
"""
Student Record System - Command Line Interface
================================================
A simple, file-backed CRUD application for managing student records.

Features:
  - Add / View / Search / Update / Delete student records
  - Persistent storage using a local JSON file (students.json)
  - Basic input validation
  - Average marks & grade calculation

Run:
    python student_record_system.py
"""

import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.json")


# --------------------------------------------------------------------------- #
# Data layer
# --------------------------------------------------------------------------- #
class StudentRecordSystem:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.students = {}  # key: roll_no (str) -> dict of student info
        self.load_data()

    # ---------- persistence ----------
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.students = json.load(f)
            except (json.JSONDecodeError, IOError):
                print("Warning: could not read existing data file. Starting fresh.")
                self.students = {}
        else:
            self.students = {}

    def save_data(self):
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.students, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    # ---------- helpers ----------
    @staticmethod
    def calculate_grade(average):
        if average >= 90:
            return "A+"
        elif average >= 80:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 60:
            return "C"
        elif average >= 50:
            return "D"
        else:
            return "F"

    # ---------- CRUD operations ----------
    def add_student(self, roll_no, name, age, student_class, marks):
        if roll_no in self.students:
            return False, f"Roll number '{roll_no}' already exists."

        average = sum(marks.values()) / len(marks) if marks else 0
        grade = self.calculate_grade(average)

        self.students[roll_no] = {
            "name": name,
            "age": age,
            "class": student_class,
            "marks": marks,
            "average": round(average, 2),
            "grade": grade,
        }
        self.save_data()
        return True, f"Student '{name}' added successfully."

    def view_all_students(self):
        return self.students

    def search_student(self, roll_no):
        return self.students.get(roll_no)

    def search_by_name(self, name_query):
        name_query = name_query.lower()
        return {
            roll: info
            for roll, info in self.students.items()
            if name_query in info["name"].lower()
        }

    def update_student(self, roll_no, **fields):
        if roll_no not in self.students:
            return False, f"No student found with roll number '{roll_no}'."

        student = self.students[roll_no]
        for key, value in fields.items():
            if value is not None and key in student:
                student[key] = value

        if "marks" in fields and fields["marks"] is not None:
            marks = student["marks"]
            average = sum(marks.values()) / len(marks) if marks else 0
            student["average"] = round(average, 2)
            student["grade"] = self.calculate_grade(average)

        self.save_data()
        return True, f"Student '{roll_no}' updated successfully."

    def delete_student(self, roll_no):
        if roll_no not in self.students:
            return False, f"No student found with roll number '{roll_no}'."
        removed = self.students.pop(roll_no)
        self.save_data()
        return True, f"Student '{removed['name']}' (Roll No: {roll_no}) deleted."

    def class_statistics(self):
        if not self.students:
            return None
        all_averages = [s["average"] for s in self.students.values()]
        return {
            "total_students": len(self.students),
            "class_average": round(sum(all_averages) / len(all_averages), 2),
            "highest": max(self.students.items(), key=lambda x: x[1]["average"]),
            "lowest": min(self.students.items(), key=lambda x: x[1]["average"]),
        }


# --------------------------------------------------------------------------- #
# CLI layer
# --------------------------------------------------------------------------- #
class CLI:
    def __init__(self):
        self.system = StudentRecordSystem()

    def run(self):
        print("=" * 55)
        print("        STUDENT RECORD MANAGEMENT SYSTEM")
        print("=" * 55)

        menu_actions = {
            "1": self.add_student,
            "2": self.view_all,
            "3": self.search_menu,
            "4": self.update_student,
            "5": self.delete_student,
            "6": self.show_statistics,
            "0": self.exit_program,
        }

        while True:
            self.print_menu()
            choice = input("Enter your choice: ").strip()
            action = menu_actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

    @staticmethod
    def print_menu():
        print("\n" + "-" * 55)
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Class Statistics")
        print("0. Exit")
        print("-" * 55)

    # ---------- input helpers ----------
    @staticmethod
    def get_non_empty_input(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("This field cannot be empty. Please try again.")

    @staticmethod
    def get_int_input(prompt, allow_blank=False):
        while True:
            value = input(prompt).strip()
            if allow_blank and value == "":
                return None
            try:
                return int(value)
            except ValueError:
                print("Please enter a valid whole number.")

    @staticmethod
    def get_marks_input():
        marks = {}
        print("Enter subject marks (leave subject name blank to finish):")
        while True:
            subject = input("  Subject name: ").strip()
            if subject == "":
                break
            score = CLI.get_int_input(f"  Marks for {subject} (0-100): ")
            if 0 <= score <= 100:
                marks[subject] = score
            else:
                print("  Marks must be between 0 and 100. Not added.")
        return marks

    # ---------- menu actions ----------
    def add_student(self):
        print("\n--- Add New Student ---")
        roll_no = self.get_non_empty_input("Roll Number: ")
        name = self.get_non_empty_input("Name: ")
        age = self.get_int_input("Age: ")
        student_class = self.get_non_empty_input("Class/Grade Level: ")
        marks = self.get_marks_input()

        success, message = self.system.add_student(roll_no, name, age, student_class, marks)
        print(("\n✔ " if success else "\n✘ ") + message)

    def view_all(self):
        print("\n--- All Students ---")
        students = self.system.view_all_students()
        if not students:
            print("No student records found.")
            return
        self.print_student_table(students)

    def search_menu(self):
        print("\n--- Search Student ---")
        print("1. By Roll Number")
        print("2. By Name")
        sub_choice = input("Choose search type: ").strip()

        if sub_choice == "1":
            roll_no = self.get_non_empty_input("Enter Roll Number: ")
            student = self.system.search_student(roll_no)
            if student:
                self.print_student_table({roll_no: student})
            else:
                print(f"No student found with roll number '{roll_no}'.")
        elif sub_choice == "2":
            name_query = self.get_non_empty_input("Enter Name (or part of it): ")
            results = self.system.search_by_name(name_query)
            if results:
                self.print_student_table(results)
            else:
                print(f"No students found matching '{name_query}'.")
        else:
            print("Invalid search option.")

    def update_student(self):
        print("\n--- Update Student ---")
        roll_no = self.get_non_empty_input("Enter Roll Number to update: ")
        student = self.system.search_student(roll_no)
        if not student:
            print(f"No student found with roll number '{roll_no}'.")
            return

        print("Leave a field blank to keep its current value.")
        name = input(f"Name [{student['name']}]: ").strip() or None
        age_input = input(f"Age [{student['age']}]: ").strip()
        age = int(age_input) if age_input else None
        student_class = input(f"Class [{student['class']}]: ").strip() or None

        update_marks = input("Update marks? (y/n): ").strip().lower()
        marks = self.get_marks_input() if update_marks == "y" else None

        success, message = self.system.update_student(
            roll_no, name=name, age=age, **{"class": student_class}, marks=marks
        )
        print(("\n✔ " if success else "\n✘ ") + message)

    def delete_student(self):
        print("\n--- Delete Student ---")
        roll_no = self.get_non_empty_input("Enter Roll Number to delete: ")
        confirm = input(f"Are you sure you want to delete '{roll_no}'? (y/n): ").strip().lower()
        if confirm == "y":
            success, message = self.system.delete_student(roll_no)
            print(("\n✔ " if success else "\n✘ ") + message)
        else:
            print("Deletion cancelled.")

    def show_statistics(self):
        print("\n--- Class Statistics ---")
        stats = self.system.class_statistics()
        if not stats:
            print("No student records found.")
            return
        highest_roll, highest_info = stats["highest"]
        lowest_roll, lowest_info = stats["lowest"]
        print(f"Total Students : {stats['total_students']}")
        print(f"Class Average  : {stats['class_average']}")
        print(f"Highest Score  : {highest_info['name']} (Roll {highest_roll}) - {highest_info['average']}")
        print(f"Lowest Score   : {lowest_info['name']} (Roll {lowest_roll}) - {lowest_info['average']}")

    def exit_program(self):
        print("\nGoodbye! All data has been saved.")
        sys.exit(0)

    # ---------- display helpers ----------
    @staticmethod
    def print_student_table(students):
        header = f"{'Roll No':<10}{'Name':<20}{'Age':<6}{'Class':<10}{'Average':<10}{'Grade':<6}"
        print(header)
        print("-" * len(header))
        for roll_no, info in students.items():
            print(
                f"{roll_no:<10}{info['name']:<20}{info['age']:<6}"
                f"{info['class']:<10}{info['average']:<10}{info['grade']:<6}"
            )


if __name__ == "__main__":
    try:
        CLI().run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Data has been saved. Goodbye!")
        sys.exit(0)