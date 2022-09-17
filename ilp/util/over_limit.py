import numpy as np
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scipy.optimize import linear_sum_assignment
from obj.site import Site

def over_limit(site, tnat, tgrade, tgender):
    result = []

    for student in opt_students(site, tnat, tgrade, tgender):
        site.remove_student(student)
        student.setSite(None)
        result += [student]
    return result

def ol_make_weights(tnat, site, student, tgrade, tgender):

    weight = 0

    if site.getName() == "X":
        return weight

    if site not in student.getPreferences():
        weight += 100

    weight += int((site.getSpecificNationality(student.getNationality())/tnat[student.getNationality()])*20)
    if student.getPrevious():
        if site in student.getPrevious():
            weight += 10
    site_genders = site.getGenders()
    site_grades = site.getGrades()

    site_grade_ratio = site_grades[student.getGrade()-9] / sum(site_grades)
    total_grade_ratio = tgrade[student.getGrade()-9] / sum(tgrade)

    if site_grade_ratio > total_grade_ratio:
        weight += int(100*(site_grade_ratio-total_grade_ratio))
    else: weight -= 10

    # other gender population at ISM is quite small
    if student.getGender() == "M": idx = 0
    else: idx = 1

    site_gender_ratio = site_genders[idx] / sum(site_genders)
    total_gender_ratio = tgender[idx] / sum(tgender)

    if site_gender_ratio > total_gender_ratio:
        weight += int(100*(site_gender_ratio-total_gender_ratio))
    else: weight -= 10

    return weight

def opt_students(site, tnat, tgrade, tgender):
    cost_matrix = []
    site_list = []
    for _ in range(site.getLimit()):
        site_list += [site]
    for _ in range(site.getTotal()-site.getLimit()):
        site_list += [Site("X", int(1e9))]
    for student in site.getStudents():
        weights = []
        for s in site_list:
            weight = ol_make_weights(tnat, s, student, tgrade, tgender)
            weights += [weight]
        cost_matrix += [weights]

    cost_matrix = np.array(cost_matrix)

    _, col_ind = linear_sum_assignment(cost_matrix)
    opt_ass = col_ind
    opt_ass = list(opt_ass)

    move_students = []
    all_students = site.getStudents()

    for i in range(site.getTotal()):
        if opt_ass[i] >= site.getLimit():
            move_students.append(all_students[i])

    return move_students