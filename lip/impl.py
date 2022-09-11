# import os

# cwd = os.getcwd() 
# files = os.listdir(cwd)
# print("Files in %r: %s" % (cwd, files))

# I DEFINITELY NEED TO REFACTOR THIS CODE AND ADD COMMENTS 
# but I think I named the variables pretty well ^^^

import csv
from algo.lsa import LSA
from obj.student import Student
from obj.site import Site
from util.tocsv import toCSV
from util.popularity import least_popular
from test.test_results import standard_deviation
from test.chart import bar, by_amt, pie, by_gender, by_grade, by_nationality

all_site_names = []
all_sites = []
total = 0
pos_allocations = {}
nationality_data = {}
total_cas_cnt = 0

f9, f10, f11, f12 = [], [], [], []
m9, m10, m11, m12 = [], [], [], []
o9, o10, o11, o12 = [], [], [], []

with open("lip/files/real_icare.csv", 'r') as f:
    reader = csv.reader(f)

    for _, line in enumerate(reader):
        for i in list(line)[1:5]:
            if i not in all_site_names:
                all_site_names += [i]
        
        nationality = line[9]

        if nationality in nationality_data:
            nationality_data[nationality] += 1
        else: nationality_data[nationality] = 1

        total += 1

    for i in all_site_names:
        all_sites += [Site(i)]
    
    f.seek(0)
    
    for _, line in enumerate(reader):
        line = list(line)
        # print(line)
        email = line[10]
        name = line[7] + " " + line[8]

        previous = []
        pref_site_names = line[1:5]
        pref_sites = []
        for i in pref_site_names:
            for j in all_sites:
                if i == j.getName():
                    pref_sites += [j]

        grade = int(line[5].split()[1])
        gender = line[6][0]

        nationality = line[9]

        cas_project, return_project = False, False

        if line[11].lower() == "yes":
            cas_project = True
            total_cas_cnt += 1
        if line[12] and line[12].lower() == "yes":
            return_project = True
        
        tmp_student = Student(email, pref_sites, nationality, 
        name, grade, gender, previous, cas_project, return_project)

        for i in pref_sites:
            if i in pos_allocations:
                pos_allocations[i].append(tmp_student)
            else: pos_allocations[i] = [tmp_student]

        if return_project:
            # print(pref_sites[0].getName(), tmp_student.getName(), "returning student")
            pref_sites[0].add_student(tmp_student)
            tmp_student.setSite(pref_sites[0])
            continue
        
        if grade == 9:
            if gender == "F":
                f9 += [tmp_student]
            elif gender == "M":
                m9 += [tmp_student]
            else:
                o9 += [tmp_student]
        elif grade == 10:
            if gender == "F":
                f10 += [tmp_student]
            elif gender == "M":
                m10 += [tmp_student]
            else:
                o10 += [tmp_student]
        elif grade == 11:
            if gender == "F":
                f11 += [tmp_student]
            elif gender == "M":
                m11+= [tmp_student]
            else:
                o11 += [tmp_student]
        else:
            if gender == "F":
                f12 += [tmp_student]
            elif gender == "M":
                m12 += [tmp_student]
            else:
                o12 += [tmp_student]

all_students = []
all_students += [f9] + [f10] + [f11] + [f12]
all_students += [m9] + [m10] + [m11] + [m12]
all_students += [o9] + [o10] + [o11] + [o12]

unassigned_students = []
# print(all_students)

for student_group in all_students:
    # print(len(all_sites), len(student_group))
    if len(student_group) >= len(all_sites):
        left = LSA.run(student_group, all_sites, nationality_data, total_cas_cnt, total)
        unassigned_students += left
    else:
        if student_group:
            unassigned_students += student_group

# print("total:", total)
if len(unassigned_students) >= len(all_sites):
    unassigned_students = LSA.run(unassigned_students, all_sites, nationality_data, total_cas_cnt, total)

if unassigned_students:
    for s in unassigned_students:
        minimum_pref = None
        minimum_amt = int(1e9)
        for pref in s.getPreferences()[::-1]:
            if pref.getTotal() <= minimum_amt:
                minimum_pref = pref
                minimum_amt = pref.getTotal()
        # print("final", minimum_pref.getName(), minimum_amt)
        minimum_pref.add_student(s)
        s.setSite(minimum_pref)

# reassign from least popular site

# pos_allocations = {}

for site in least_popular(all_sites):
    for pos_student in pos_allocations[site]:
        if pos_student not in site.getStudents():
            assigned_site = pos_student.getSite()
            if assigned_site.getTotal() > site.getTotal():
                assigned_site.remove_student(pos_student)
                pos_student.setSite(site)
                site.add_student(pos_student)

results = {}
check = []

for site in all_sites:
    students = site.getStudents()
    # for s in students:
    #     print(s.getName(), site.getName(), s.getNationality())
    results[site.getName()] = students
    check += [site.getTotal()]

print(standard_deviation(check))

most_popular_site = least_popular(all_sites)[len(all_sites)-1]
least_popular_site = least_popular(all_sites)[0]

print(most_popular_site.getName())

pie(by_nationality(most_popular_site)[0], by_nationality(most_popular_site)[1])

toCSV(results)

# by now all students should be assigned and it should be optimal!!