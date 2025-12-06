class Student:
    def __init__(self, student_id, name, section):
        self.student_id = student_id
        self.name = name
        self.section = section
        self.enrolled_subjects = []
    
    def enroll_subject(self, subject_code):
        if subject_code not in self.enrolled_subjects:
            self.enrolled_subjects.append(subject_code)
    
    def get_num_subjects(self):
        return len(self.enrolled_subjects)
    
    def to_file_string(self):
        return f"{self.student_id}|{self.name}|{self.section}\n"
    
    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Section: {self.section}, Subjects: {self.get_num_subjects()}"