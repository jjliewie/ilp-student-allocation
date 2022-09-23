import csv
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from obj.student import Student

e_idx, n_idx, g_idx, gr_idx, na_idx = 7, [4, 1], 5, 0, 6

def compile_others(submitted_students):

    with open('ilp/files/all_students.csv', 'r') as f:
        others = []
        reader = csv.reader(f)
        email_list = []
        for students in submitted_students:
            for student in students:
                email_list.append(student.getEmail().lower().strip())

        for i, line in enumerate(reader):
            if i == 0: continue
            email = line[e_idx]
            if email.lower() not in email_list:
                name = line[n_idx[0]] + " " + line[n_idx[1]]
                grade = int(line[gr_idx])
                gender = line[g_idx]
                nationality = line[na_idx].split("(")[0].strip()
                tmp_student = Student(email, [], nationality, 
                name, grade, gender, [], False, False)
                others += [tmp_student]
    
    f.close()

    return others