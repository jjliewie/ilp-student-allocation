import csv
from algo.lsa import LSA
from obj.student import Student
from obj.site import Site
from util.tocsv import toCSV
from util.popularity import least_popular
from test.test_results import standard_deviation
from impl_other import impl_other
from util.over_limit import over_limit
from util.best_possible_site import assign_students
from util.availability import availability

all_sites = []
total = 0
pos_allocations = {}
nationality_data = {}
total_cas_cnt = 0
gender_data = [0, 0, 0]
# male, female, other
grade_data = [0, 0, 0, 0]
# 9, 10, 11, 12

f9, f10, f11, f12 = [], [], [], []
m9, m10, m11, m12 = [], [], [], []
o9, o10, o11, o12 = [], [], [], []

# initialization

# metro
with open("lip/files/metro_icare.csv", 'r') as m:
    reader = csv.reader(m)
    for line in reader:
        site_name = line[1]
        site_cap = int(line[2])
        all_sites += [Site(site_name, site_cap)]
m.close()

# print(len(all_sites))

# provincial
with open("lip/files/provincial_icare.csv", 'r') as p:
    reader = csv.reader(p)
    for line in reader:
        site_name = line[1]
        site_cap = int(line[2])
        all_sites += [Site(site_name, site_cap)]
p.close()

# print(len(all_sites))

with open("lip/files/real_icare.csv", 'r') as f:
    reader = csv.reader(f)
    
    for line in reader:
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

        if nationality in nationality_data:
            nationality_data[nationality] += 1
        else: nationality_data[nationality] = 1

        total += 1

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
                pos_allocations[i] += [tmp_student]
            else: pos_allocations[i] = [tmp_student]

        if return_project:
            pref_sites[0].add_student(tmp_student)
            tmp_student.setSite(pref_sites[0])
            continue
    
        grade_data[grade-9] += 1
        
        if grade == 9:
            if gender == "F":
                f9 += [tmp_student]
                gender_data[1] += 1
            elif gender == "M":
                m9 += [tmp_student]
                gender_data[0] += 1
            else:
                o9 += [tmp_student]
                gender_data[2] += 1
        elif grade == 10:
            if gender == "F":
                f10 += [tmp_student]
                gender_data[1] += 1
            elif gender == "M":
                m10 += [tmp_student]
                gender_data[0] += 1
            else:
                o10 += [tmp_student]
                gender_data[2] += 1
        elif grade == 11:
            if gender == "F":
                f11 += [tmp_student]
                gender_data[0] += 1
            elif gender == "M":
                m11+= [tmp_student]
                gender_data[1] += 1
            else:
                o11 += [tmp_student]
                gender_data[2] += 1
        else:
            if gender == "F":
                f12 += [tmp_student]
                gender_data[1] += 1
            elif gender == "M":
                m12 += [tmp_student]
                gender_data[0] += 1
            else:
                o12 += [tmp_student]
                gender_data[2] += 1

f.close()

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

# print(pos_allocations)

for site in least_popular(all_sites):
    for pos_student in pos_allocations[site]:
        if pos_student not in site.getStudents() and not pos_student.senior_returning():
            assigned_site = pos_student.getSite()
            if assigned_site.getTotal() > site.getTotal():
                assigned_site.remove_student(pos_student)
                pos_student.setSite(site)
                site.add_student(pos_student)

again_student = []
for site in all_sites:
    again_student += over_limit(site, nationality_data, grade_data, gender_data)

assign_students(availability(all_sites), again_student, nationality_data, grade_data, gender_data)

other_students, other_sites = impl_other(least_popular(availability(all_sites)))
# change nationality_data & total_cas_cnt & total
just_check = LSA.run(other_students, other_sites, nationality_data, total_cas_cnt, total)

results = {}
check = []

for site in all_sites:
    students = site.getStudents()
    results[site.getName()] = students
    check += [site.getTotal()]

    # if site.getTotal() != len(site.getStudents()):
    #     print("WHY", site.getTotal(), site.getName(), len(site.getStudents()))

print(standard_deviation(check))

most_popular_site = least_popular(all_sites)[len(all_sites)-1]
least_popular_site = least_popular(all_sites)[0]
print(least_popular_site.getName(), least_popular_site.getTotal())
print(most_popular_site.getName(), most_popular_site.getTotal())

# pie(by_nationality(most_popular_site)[0], by_nationality(most_popular_site)[1])

# print(sum(check), "check")

toCSV(results)

# by now all students should be assigned and it should be optimal!!