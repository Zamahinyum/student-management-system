# Student Management System

A comprehensive Python-based Student Management System built using Object-Oriented Programming principles. This system allows users to manage students, subjects, enrollments, grades, and attendance through an interactive command-line interface.

## Features Implemented

### Core Features
- **Student Management**: Add students with unique IDs, names, and sections
- **Subject Management**: Add subjects with codes, names, and credit hours
- **Enrollment System**: Enroll students in multiple subjects
- **Grade Management**: Add and track multiple grades per subject
- **Attendance Tracking**: Mark attendance and calculate percentages
- **Reporting System**: Generate detailed student reports with performance metrics

### Additional Features
- Automatic data persistence using text files
- Average grade calculation per subject
- Attendance percentage calculation
- Overall performance summaries
- Data validation and error handling
- Clean, formatted output

## Project Structure

```
student_management_system/
├── main.py                 # Entry point with interactive menu
├── models/
│   ├── student.py         # Student class
│   ├── subject.py         # Subject class
│   ├── record.py          # Record class (grades + attendance)
│   └── manager.py         # SystemManager class (core logic)
├── data/
│   ├── students.txt       # Student records
│   ├── subjects.txt       # Subject records
│   ├── enrollments.txt    # Enrollment mappings
│   └── records.txt        # Grade and attendance records
└── README.md              # This file
```

## How to Run the System

### Prerequisites
- Python 3.6 or higher
- Anaconda PowerShell (or any terminal)

## Classes Overview

### Student Class (`student.py`)
- **Attributes**: student_id, name, section, enrolled_subjects
- **Methods**: enroll_subject(), get_num_subjects(), to_file_string(), from_file_string()

### Subject Class (`subject.py`)
- **Attributes**: subject_code, subject_name, credit_hours
- **Methods**: to_file_string(), from_file_string()

### Record Class (`record.py`)
- **Attributes**: student_id, subject_code, grades[], attendance_present, attendance_total
- **Methods**: add_grade(), get_average_grade(), mark_attendance(), get_attendance_percentage()

### SystemManager Class (`manager.py`)
- **Core Operations**: 
  - add_student(), add_subject(), enroll_student()
  - add_grade(), mark_attendance()
  - generate_student_report(), view_all_students()
- **Data Persistence**: 
  - save_students(), save_subjects(), save_records(), save_enrollments()
  - load_all_data()

## Usage Examples

### Adding a Student
1. Select option 1 from menu
2. Enter student ID 
3. Enter name
4. Enter section

### Enrolling a Student
1. Select option 3 from menu
2. Enter student ID
3. Enter subject code
4. System automatically creates a record

### Viewing Reports
1. Select option 6 from menu
2. Enter student ID
3. View detailed report with grades and attendance
