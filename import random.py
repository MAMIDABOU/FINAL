import random
import string
import time
from bisect import bisect_left
import os
import csv

# Student Class 
# This class defines a Student with attributes: name, ID, score, and attendance
class Student:
    def __init__(self, name, student_id, score, attendance):
        self.name = name
        self.student_id = student_id
        self.score = score
        self.attendance = attendance

    # Readable string representation when printing a Student
    def __repr__(self):
        return f"Student(Name: {self.name}, ID: {self.student_id}, Score: {self.score}, Attendance: {self.attendance})"

#  StudentManager Class 
# A collection of Student oinformation and provides search, sort, and analysis tools
class StudentManager:
    def __init__(self):
        self.students = []

    # Add a student to the list
    def add_student(self, student):
        self.students.append(student)

    # Print all student records
    def print_all_students(self):
        for student in self.students:
            print(student)

    # Linear search for a student by name (O(n))
    def linear_search_by_name(self, name):
        for student in self.students:
            if student.name == name:
                return student
        return None

    # Sort students by score (ascending order) (O(n log n))
    def sort_students_by_score(self):
        self.students.sort(key=lambda student: student.score)

    # Binary search for a student by score (requires sorting first) (O(log n))
    def binary_search_by_score(self, score):
        self.sort_students_by_score()
        scores = [student.score for student in self.students]
        index = bisect_left(scores, score)
        if index != len(scores) and scores[index] == score:
            return self.students[index]
        return None

    # Get top N students with the highest scores
    def get_top_n_students(self, n):
        self.sort_students_by_score()
        return self.students[-n:]

    # Calculate average score for the class
    def average_score(self):
        if not self.students:
            return 0
        total_score = sum(student.score for student in self.students)
        return total_score / len(self.students)

# Loads students from a CSV file. If the file doesn't exist or fails, it generates random data.
def load_students_from_file(file_path):
    manager = StudentManager()

    # If the file is a CSV, try loading it
    if file_path.endswith('.csv'):
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row["Name"]
                    student_id = int(row["Student_ID"])
                    score = int(row["Score"])
                    attendance = int(row["Attendance"])
                    manager.add_student(Student(name, student_id, score, attendance))
        except Exception as e:
            print(f"Error loading CSV: {e}")
    else:
        # If no file is provided or it's not a CSV, generate 10,000 random students
        print(f"Generating 10,000 random students...")
        for i in range(10000):
            name = ''.join(random.choices(string.ascii_letters, k=6))
            student_id = random.randint(100, 10000)
            score = random.randint(0, 100)
            attendance = random.randint(50, 100)
            manager.add_student(Student(name, student_id, score, attendance))

    return manager

#  Performance Measuring Function 
# Measures and prints the time taken for linear and binary searches
def measure_search_performance(student_manager, search_name, search_score):
    # Measure linear search by name
    start = time.time()
    result_name = student_manager.linear_search_by_name(search_name)
    linear_search_time = time.time() - start
    print(f"Linear Search Time: {linear_search_time:.6f}s")
    if result_name:
        print(f"Result: {result_name}")
    else:
        print(f"No student found with name: {search_name}")

    # Measure time to sort the students
    start = time.time()
    student_manager.sort_students_by_score()
    sort_time = time.time() - start
    print(f"Sort Time: {sort_time:.6f}s")

    # Measure binary search by score
    start = time.time()
    result_score = student_manager.binary_search_by_score(search_score)
    binary_search_time = time.time() - start
    print(f"Binary Search Time: {binary_search_time:.6f}s")
    if result_score:
        print(f"Result: {result_score}")
    else:
        print(f"No student found with score: {search_score}")

    return {
        "Linear Search Time": linear_search_time,
        "Binary Search Time": binary_search_time,
        "Sort Time": sort_time
    }

#  Main Program 

# Set path to your student CSV file
csv_file = "D:\\sample_student_data.csv"

# Load data from CSV if file exists, otherwise generate random student data
if os.path.exists(csv_file):
    student_manager = load_students_from_file(csv_file)
else:
    student_manager = load_students_from_file("")

# Choose a sample name and score for testing
if student_manager.students:
    test_name = student_manager.students[0].name  # Use first student's name
    middle_index = len(student_manager.students) // 2
    test_score = student_manager.students[middle_index].score  # Use a score from the middle
else:
    test_name = "TestName"
    test_score = 50

# Run search performance tests
print(f"Searching for student with name: {test_name}")
performance_results = measure_search_performance(student_manager, test_name, test_score)

# Display top 5 students by score
print("\nTop 5 Students:")
start = time.time()
top_students = student_manager.get_top_n_students(5)
top_time = time.time() - start
print(f"Sort Time: {top_time:.6f}s")
for student in top_students:
    print(student)

# Calculate and display average class score
start = time.time()
avg_score = student_manager.average_score()
avg_time = time.time() - start
print(f"Average Score Calculation Time: {avg_time:.6f}s")
print(f"Average Score: {avg_score:.2f}")
