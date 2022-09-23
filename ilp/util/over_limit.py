import numpy as np
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scipy.optimize import linear_sum_assignment
from obj.site import Site

def over_limit(site, tnat):
    result = []
    specific = site.getSpecific()

    cap_by_gr_ge = [
        [0, 0, 0],  
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    for gr in range(len(specific)):
        for ge in range(len(specific[gr])):
            if site.getLimit()//8 < specific[gr][ge]:
                cap_by_gr_ge[gr][ge] = (site.getLimit()//8)

    students_by_gr_ge = [
        [[], [], []],  
        [[], [], []],
        [[], [], []],  
        [[], [], []]
    ]

    for s in site.getStudents():
        idx = 2
        if s.getGender() == "M": idx = 0
        elif s.getGender() == "F": idx = 1
        students_by_gr_ge[s.getGrade()-9][idx].append(s)

    for group in range(4):
        for gender_group in range(3):
            sp_group = students_by_gr_ge[group][gender_group]
            if sp_group and cap_by_gr_ge[group][gender_group]:
                for student in opt_students(site, tnat, sp_group, cap_by_gr_ge[group][gender_group]):
                    site.remove_student(student)
                    student.setSite(None)
                    result += [student]
    final = []
    if site.getTotal() < site.getLimit():
        if result:
            for student in opt_students(site, tnat, result, site.getLimit()-site.getTotal()):
                final += [student]
    
    for r in result:
        if r not in final:
            site.add_student(r)
            r.setSite(site)

    return final

def ol_make_weights(tnat, site, student):
    weight = 0
    if site.getName() == "X":
        return weight
    if site not in student.getPreferences():
        weight += 100
    weight += int((site.getSpecificNationality(student.getNationality())/tnat[student.getNationality()])*40)
    return weight

def opt_students(site, tnat, students, cap):

    cost_matrix = []
    site_list = []
    for _ in range(cap):
        site_list += [site]
    for _ in range(len(students)-cap):
        site_list += [Site("X", int(1e9))]

    for student in students:
        weights = []
        for s in site_list:
            weight = ol_make_weights(tnat, s, student)
            weights += [weight]
        cost_matrix += [weights]

    cost_matrix = np.array(cost_matrix)

    _, col_ind = linear_sum_assignment(cost_matrix)
    opt_ass = col_ind
    opt_ass = list(opt_ass)

    move_students = []
    all_students = students

    for i in range(len(students)):
        if opt_ass[i] >= cap:
            move_students.append(all_students[i])

    return move_students