import os
from models.student import Student
from models.subject import Subject
from models.record import Record

class SystemManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.students = {}
        self.subjects = {}
        self.records = []
        self._ensure_data_dir()
        self.load_all_data()
    
    def _ensure_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        files = ['students.txt', 'subjects.txt', 'enrollments.txt', 'records.txt']
        for file in files:
            filepath = os.path.join(self.data_dir, file)
            if not os.path.exists(filepath):
                open(filepath, 'w').close()
    
    def add_student(self, student_id, name, section):
        if student_id in self.students:
            print(f"Error: Student ID {student_id} already exists.")
            return False
        student = Student(student_id, name, section)
        self.students[student_id] = student
        self.save_students()
        print(f"Student {name} added successfully!")
        return True
    
    def add_subject(self, subject_code, subject_name, credit_hours):
        if subject_code in self.subjects:
            print(f"Error: Subject code {subject_code} already exists.")
            return False
        subject = Subject(subject_code, subject_name, credit_hours)
        self.subjects[subject_code] = subject
        self.save_subjects()
        print(f"Subject {subject_name} added successfully!")
        return True
    
    def enroll_student(self, student_id, subject_code):
        if student_id not in self.students:
            print(f"Error: Student ID {student_id} not found.")
            return False
        if subject_code not in self.subjects:
            print(f"Error: Subject code {subject_code} not found.")
            return False
        
        for record in self.records:
            if record.student_id == student_id and record.subject_code == subject_code:
                print(f"Error: Student already enrolled in this subject.")
                return False
        
        self.students[student_id].enroll_subject(subject_code)
        new_record = Record(student_id, subject_code)
        self.records.append(new_record)
        self.save_enrollments()
        self.save_records()
        print(f"Student {student_id} enrolled in {subject_code} successfully!")
        return True
    
    def add_grade(self, student_id, subject_code, grade):
        record = self._find_record(student_id, subject_code)
        if not record:
            print(f"Error: Enrollment record not found.")
            return False
        
        try:
            grade_val = float(grade)
            if grade_val < 0 or grade_val > 100:
                print("Error: Grade must be between 0 and 100.")
                return False
            record.add_grade(grade_val)
            self.save_records()
            print(f"Grade {grade_val} added successfully!")
            return True
        except ValueError:
            print("Error: Invalid grade value.")
            return False
    
    def mark_attendance(self, student_id, subject_code, present=True):
        record = self._find_record(student_id, subject_code)
        if not record:
            print(f"Error: Enrollment record not found.")
            return False
        
        record.mark_attendance(present)
        self.save_records()
        status = "present" if present else "absent"
        print(f"Attendance marked as {status}!")
        return True
    
    def _find_record(self, student_id, subject_code):
        for record in self.records:
            if record.student_id == student_id and record.subject_code == subject_code:
                return record
        return None
    
    def generate_student_report(self, student_id):
        if student_id not in self.students:
            print(f"Error: Student ID {student_id} not found.")
            return
        
        student = self.students[student_id]
        print("\n" + "="*60)
        print(f"STUDENT REPORT")
        print("="*60)
        print(f"Student ID: {student.student_id}")
        print(f"Name: {student.name}")
        print(f"Section: {student.section}")
        print(f"Total Subjects Enrolled: {student.get_num_subjects()}")
        print("-"*60)
        
        student_records = [r for r in self.records if r.student_id == student_id]
        
        if not student_records:
            print("No enrollment records found.")
            print("="*60 + "\n")
            return
        
        total_grade = 0
        total_attendance = 0
        count = 0
        
        print(f"{'Subject Code':<15} {'Subject Name':<25} {'Avg Grade':<12} {'Attendance'}")
        print("-"*60)
        
        for record in student_records:
            subject = self.subjects.get(record.subject_code)
            subject_name = subject.subject_name if subject else "Unknown"
            avg_grade = record.get_average_grade()
            attendance = record.get_attendance_percentage()
            
            print(f"{record.subject_code:<15} {subject_name:<25} {avg_grade:>6.2f}      {attendance:>6.1f}%")
            
            if avg_grade > 0:
                total_grade += avg_grade
                count += 1
            total_attendance += attendance
        
        print("-"*60)
        
        if count > 0:
            overall_avg = total_grade / count
            print(f"Overall Average Grade: {overall_avg:.2f}")
        
        if len(student_records) > 0:
            overall_attendance = total_attendance / len(student_records)
            print(f"Overall Attendance: {overall_attendance:.1f}%")
        
        gpa = self.get_student_gpa(student_id)
        print(f"GPA: {gpa:.2f}")
        
        print("="*60 + "\n")
    
    def view_all_students(self):
        if not self.students:
            print("No students in the system.")
            return
        
        print("\n" + "="*60)
        print("ALL STUDENTS")
        print("="*60)
        for student in self.students.values():
            print(student)
        print("="*60 + "\n")
    
    def get_student_gpa(self, student_id):
        student_records = [r for r in self.records if r.student_id == student_id]
        if not student_records:
            return 0.0
        
        total_points = 0
        total_credits = 0
        
        for record in student_records:
            avg_grade = record.get_average_grade()
            if avg_grade > 0:
                subject = self.subjects.get(record.subject_code)
                if subject:
                    gpa_points = self.grade_to_gpa(avg_grade)
                    total_points += gpa_points * subject.credit_hours
                    total_credits += subject.credit_hours
        
        if total_credits == 0:
            return 0.0
        return total_points / total_credits
    
    def grade_to_gpa(self, grade):
        if grade >= 90:
            return 4.0
        elif grade >= 85:
            return 3.7
        elif grade >= 80:
            return 3.3
        elif grade >= 75:
            return 3.0
        elif grade >= 70:
            return 2.7
        elif grade >= 65:
            return 2.3
        elif grade >= 60:
            return 2.0
        elif grade >= 55:
            return 1.7
        elif grade >= 50:
            return 1.0
        else:
            return 0.0
    
    def view_student_rankings(self):
        if not self.students:
            print("No students in the system.")
            return
        
        student_gpas = []
        for student_id in self.students:
            gpa = self.get_student_gpa(student_id)
            student_gpas.append((student_id, gpa))
        
        student_gpas.sort(key=lambda x: x[1], reverse=True)
        
        print("\n" + "="*70)
        print("STUDENT RANKINGS (BY GPA)")
        print("="*70)
        print(f"{'Rank':<8} {'Student ID':<15} {'Name':<25} {'GPA':<10}")
        print("-"*70)
        
        for rank, (student_id, gpa) in enumerate(student_gpas, 1):
            student = self.students[student_id]
            print(f"{rank:<8} {student_id:<15} {student.name:<25} {gpa:.2f}")
        
        print("="*70 + "\n")
    
    def view_subject_statistics(self):
        if not self.subjects:
            print("No subjects in the system.")
            return
        
        print("\n" + "="*80)
        print("SUBJECT-WISE STATISTICS")
        print("="*80)
        print(f"{'Subject Code':<15} {'Subject Name':<25} {'Enrolled':<12} {'Avg Grade':<12} {'Avg Attend'}")
        print("-"*80)
        
        for subject_code, subject in self.subjects.items():
            subject_records = [r for r in self.records if r.subject_code == subject_code]
            
            if not subject_records:
                enrolled = 0
                avg_grade = 0.0
                avg_attendance = 0.0
            else:
                enrolled = len(subject_records)
                total_grade = sum([r.get_average_grade() for r in subject_records if r.get_average_grade() > 0])
                count_grade = len([r for r in subject_records if r.get_average_grade() > 0])
                avg_grade = total_grade / count_grade if count_grade > 0 else 0.0
                
                total_attendance = sum([r.get_attendance_percentage() for r in subject_records])
                avg_attendance = total_attendance / enrolled if enrolled > 0 else 0.0
            
            print(f"{subject_code:<15} {subject.subject_name:<25} {enrolled:<12} {avg_grade:>6.2f}      {avg_attendance:>6.1f}%")
        
        print("="*80 + "\n")
    
    def delete_student(self, student_id):
        if student_id not in self.students:
            print(f"Error: Student ID {student_id} not found.")
            return False
        
        del self.students[student_id]
        self.records = [r for r in self.records if r.student_id != student_id]
        self.save_students()
        self.save_records()
        self.save_enrollments()
        print(f"Student {student_id} deleted successfully!")
        return True
    
    def delete_subject(self, subject_code):
        if subject_code not in self.subjects:
            print(f"Error: Subject code {subject_code} not found.")
            return False
        
        del self.subjects[subject_code]
        self.records = [r for r in self.records if r.subject_code != subject_code]
        
        for student in self.students.values():
            if subject_code in student.enrolled_subjects:
                student.enrolled_subjects.remove(subject_code)
        
        self.save_subjects()
        self.save_records()
        self.save_enrollments()
        print(f"Subject {subject_code} deleted successfully!")
        return True
    
    def unenroll_student(self, student_id, subject_code):
        if student_id not in self.students:
            print(f"Error: Student ID {student_id} not found.")
            return False
        
        record_found = False
        for record in self.records:
            if record.student_id == student_id and record.subject_code == subject_code:
                self.records.remove(record)
                record_found = True
                break
        
        if not record_found:
            print(f"Error: Enrollment record not found.")
            return False
        
        if subject_code in self.students[student_id].enrolled_subjects:
            self.students[student_id].enrolled_subjects.remove(subject_code)
        
        self.save_records()
        self.save_enrollments()
        print(f"Student {student_id} unenrolled from {subject_code} successfully!")
        return True
    
    def export_student_report(self, student_id):
        if student_id not in self.students:
            print(f"Error: Student ID {student_id} not found.")
            return False
        
        student = self.students[student_id]
        filename = f"report_{student_id}.txt"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("="*60 + "\n")
            f.write("STUDENT REPORT\n")
            f.write("="*60 + "\n")
            f.write(f"Student ID: {student.student_id}\n")
            f.write(f"Name: {student.name}\n")
            f.write(f"Section: {student.section}\n")
            f.write(f"Total Subjects Enrolled: {student.get_num_subjects()}\n")
            f.write("-"*60 + "\n")
            
            student_records = [r for r in self.records if r.student_id == student_id]
            
            if not student_records:
                f.write("No enrollment records found.\n")
                f.write("="*60 + "\n")
            else:
                f.write(f"{'Subject Code':<15} {'Subject Name':<25} {'Avg Grade':<12} {'Attendance'}\n")
                f.write("-"*60 + "\n")
                
                total_grade = 0
                total_attendance = 0
                count = 0
                
                for record in student_records:
                    subject = self.subjects.get(record.subject_code)
                    subject_name = subject.subject_name if subject else "Unknown"
                    avg_grade = record.get_average_grade()
                    attendance = record.get_attendance_percentage()
                    
                    f.write(f"{record.subject_code:<15} {subject_name:<25} {avg_grade:>6.2f}      {attendance:>6.1f}%\n")
                    
                    if avg_grade > 0:
                        total_grade += avg_grade
                        count += 1
                    total_attendance += attendance
                
                f.write("-"*60 + "\n")
                
                if count > 0:
                    overall_avg = total_grade / count
                    f.write(f"Overall Average Grade: {overall_avg:.2f}\n")
                
                if len(student_records) > 0:
                    overall_attendance = total_attendance / len(student_records)
                    f.write(f"Overall Attendance: {overall_attendance:.1f}%\n")
                
                gpa = self.get_student_gpa(student_id)
                f.write(f"GPA: {gpa:.2f}\n")
                
                f.write("="*60 + "\n")
        
        print(f"Report exported successfully to {filepath}")
        return True
    
    def save_students(self):
        filepath = os.path.join(self.data_dir, 'students.txt')
        with open(filepath, 'w') as f:
            for student in self.students.values():
                f.write(student.to_file_string())
    
    def save_subjects(self):
        filepath = os.path.join(self.data_dir, 'subjects.txt')
        with open(filepath, 'w') as f:
            for subject in self.subjects.values():
                f.write(subject.to_file_string())
    
    def save_enrollments(self):
        filepath = os.path.join(self.data_dir, 'enrollments.txt')
        with open(filepath, 'w') as f:
            for student in self.students.values():
                for subject_code in student.enrolled_subjects:
                    f.write(f"{student.student_id}|{subject_code}\n")
    
    def save_records(self):
        filepath = os.path.join(self.data_dir, 'records.txt')
        with open(filepath, 'w') as f:
            for record in self.records:
                f.write(record.to_file_string())
    
    def load_all_data(self):
        self.load_students()
        self.load_subjects()
        self.load_records()
        self.load_enrollments()
    
    def load_students(self):
        filepath = os.path.join(self.data_dir, 'students.txt')
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if line.strip():
                        student = self.create_student_from_file(line)
                        self.students[student.student_id] = student
        except FileNotFoundError:
            pass
    
    def create_student_from_file(self, line):
        parts = line.strip().split('|')
        return Student(parts[0], parts[1], parts[2])
    
    def load_subjects(self):
        filepath = os.path.join(self.data_dir, 'subjects.txt')
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if line.strip():
                        subject = self.create_subject_from_file(line)
                        self.subjects[subject.subject_code] = subject
        except FileNotFoundError:
            pass
    
    def create_subject_from_file(self, line):
        parts = line.strip().split('|')
        return Subject(parts[0], parts[1], int(parts[2]))
    
    def load_records(self):
        filepath = os.path.join(self.data_dir, 'records.txt')
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if line.strip():
                        record = self.create_record_from_file(line)
                        self.records.append(record)
        except FileNotFoundError:
            pass
    
    def create_record_from_file(self, line):
        parts = line.strip().split('|')
        record = Record(parts[0], parts[1])
        if parts[2]:
            record.grades = [float(g) for g in parts[2].split(',') if g]
        record.attendance_present = int(parts[3])
        record.attendance_total = int(parts[4])
        return record
    
    def load_enrollments(self):
        filepath = os.path.join(self.data_dir, 'enrollments.txt')
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('|')
                        student_id = parts[0]
                        subject_code = parts[1]
                        if student_id in self.students:
                            self.students[student_id].enroll_subject(subject_code)
        except FileNotFoundError:
            pass