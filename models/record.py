class Record:
    def __init__(self, student_id, subject_code):
        self.student_id = student_id
        self.subject_code = subject_code
        self.grades = []
        self.attendance_present = 0
        self.attendance_total = 0
    
    def add_grade(self, grade):
        self.grades.append(float(grade))
    
    def get_average_grade(self):
        if len(self.grades) == 0:
            return 0.0
        return sum(self.grades) / len(self.grades)
    
    def mark_attendance(self, present=True):
        self.attendance_total += 1
        if present:
            self.attendance_present += 1
    
    def get_attendance_percentage(self):
        if self.attendance_total == 0:
            return 0.0
        return (self.attendance_present / self.attendance_total) * 100
    
    def to_file_string(self):
        grades_str = ','.join(map(str, self.grades))
        return f"{self.student_id}|{self.subject_code}|{grades_str}|{self.attendance_present}|{self.attendance_total}\n"
    
    def __str__(self):
        return f"Student: {self.student_id}, Subject: {self.subject_code}, Avg Grade: {self.get_average_grade():.2f}, Attendance: {self.get_attendance_percentage():.1f}%"