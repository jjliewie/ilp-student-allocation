import numpy as np
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scipy.optimize import linear_sum_assignment
from obj.site import Site

def make_weights(tnat, site, student, tgrade, tgender):

    weight = 0

    if site in student.getPreferences():
        weight -= 50

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

    if student.want_provincial() and site.isMetro():
        weight += 100
    if student.want_metro() and site.isProvincial():
        weight += 1000

    return weight

def assign_students(sites, students, tnat, tgrade, tgender):
    all_sites = []
    for site in sites:
        for _ in range(site.getLimit()-site.getTotal()):
            all_sites += [site]
    
    cost_matrix = []
    for student in students:
        weights = []
        for site in all_sites:
            weight = make_weights(tnat, site, student, tgrade, tgender)
            weights += [weight]
        cost_matrix += [weights]
    
    for _ in range(len(all_sites)-len(students)):
        cost_matrix += [len(all_sites)*[0]]

    cost_matrix = np.array(cost_matrix)
    _, col_ind = linear_sum_assignment(cost_matrix)
    opt_ass = col_ind
    opt_ass = list(opt_ass)

    for i in range(len(students)):
        assignment = all_sites[opt_ass[i]]
        assignment.add_student(students[i])
        students[i].setSite(assignment)

