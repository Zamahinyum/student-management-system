class Subject:
    def __init__(self, subject_code, subject_name, credit_hours):
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.credit_hours = int(credit_hours)
    
    def to_file_string(self):
        return f"{self.subject_code}|{self.subject_name}|{self.credit_hours}\n"
    
    def __str__(self):
        return f"Code: {self.subject_code}, Name: {self.subject_name}, Credits: {self.credit_hours}"