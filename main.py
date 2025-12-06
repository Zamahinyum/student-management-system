from models.manager import SystemManager

def display_menu():
    print("\n" + "="*50)
    print("STUDENT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add Student")
    print("2. Add Subject")
    print("3. Enroll Student")
    print("4. Add Grade")
    print("5. Mark Attendance")
    print("6. View Student Report")
    print("7. View All Students")
    print("8. View Student Rankings")
    print("9. View Subject Statistics")
    print("10. Delete Student")
    print("11. Delete Subject")
    print("12. Unenroll Student")
    print("13. Export Student Report")
    print("14. Exit")
    print("="*50)

def main():
    manager = SystemManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-14): ").strip()
        
        if choice == '1':
            print("\n--- Add Student ---")
            student_id = input("Enter Student ID: ").strip()
            name = input("Enter Student Name: ").strip()
            section = input("Enter Section/Batch: ").strip()
            manager.add_student(student_id, name, section)
        
        elif choice == '2':
            print("\n--- Add Subject ---")
            subject_code = input("Enter Subject Code: ").strip()
            subject_name = input("Enter Subject Name: ").strip()
            credit_hours = input("Enter Credit Hours: ").strip()
            try:
                manager.add_subject(subject_code, subject_name, int(credit_hours))
            except ValueError:
                print("Error: Credit hours must be a number.")
        
        elif choice == '3':
            print("\n--- Enroll Student ---")
            student_id = input("Enter Student ID: ").strip()
            subject_code = input("Enter Subject Code: ").strip()
            manager.enroll_student(student_id, subject_code)
        
        elif choice == '4':
            print("\n--- Add Grade ---")
            student_id = input("Enter Student ID: ").strip()
            subject_code = input("Enter Subject Code: ").strip()
            grade = input("Enter Grade (0-100): ").strip()
            manager.add_grade(student_id, subject_code, grade)
        
        elif choice == '5':
            print("\n--- Mark Attendance ---")
            student_id = input("Enter Student ID: ").strip()
            subject_code = input("Enter Subject Code: ").strip()
            status = input("Present? (y/n): ").strip().lower()
            present = status == 'y'
            manager.mark_attendance(student_id, subject_code, present)
        
        elif choice == '6':
            print("\n--- View Student Report ---")
            student_id = input("Enter Student ID: ").strip()
            manager.generate_student_report(student_id)
        
        elif choice == '7':
            manager.view_all_students()
        
        elif choice == '8':
            manager.view_student_rankings()
        
        elif choice == '9':
            manager.view_subject_statistics()
        
        elif choice == '10':
            print("\n--- Delete Student ---")
            student_id = input("Enter Student ID to delete: ").strip()
            confirm = input(f"Are you sure you want to delete student {student_id}? (y/n): ").strip().lower()
            if confirm == 'y':
                manager.delete_student(student_id)
        
        elif choice == '11':
            print("\n--- Delete Subject ---")
            subject_code = input("Enter Subject Code to delete: ").strip()
            confirm = input(f"Are you sure you want to delete subject {subject_code}? (y/n): ").strip().lower()
            if confirm == 'y':
                manager.delete_subject(subject_code)
        
        elif choice == '12':
            print("\n--- Unenroll Student ---")
            student_id = input("Enter Student ID: ").strip()
            subject_code = input("Enter Subject Code: ").strip()
            manager.unenroll_student(student_id, subject_code)
        
        elif choice == '13':
            print("\n--- Export Student Report ---")
            student_id = input("Enter Student ID: ").strip()
            manager.export_student_report(student_id)
        
        elif choice == '14':
            print("\nThank you for using Student Management System!")
            print("Exiting...")
            break
        
        else:
            print("\nInvalid choice! Please enter a number between 1 and 14.")

if __name__ == "__main__":
    main()