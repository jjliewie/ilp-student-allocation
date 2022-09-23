import csv
from algo.lsa import LSA
from obj.student import Student
from obj.site import Site
from util.tocsv import toCSV
from util.popularity import least_popular, most_available
from test.test_results import standard_deviation
from impl_other import impl_other
from util.over_limit import over_limit
from util.best_possible_site import assign_students
from util.availability import availability
from util.toxlsx import toXLSX
from util.importance import is_important, too_frequent
from util.basic_other import make_other, unassigned_other

all_sites = []
total = 0
pos_allocations = {}
nationality_data = {}
total_cas_cnt = 0
gender_data = [0, 0, 0]
# male, female, other
grade_data = [0, 0, 0, 0]
# 9, 10, 11, 12

e_idx, n_idx, na_idx = 1, [2, 3], 5
g_idx, gr_idx, c_idx, r_idx, p_idx = 4, 6, 7, 8, [9, 13]

f9, f10, f11, f12 = [], [], [], []
m9, m10, m11, m12 = [], [], [], []
o9, o10, o11, o12 = [], [], [], []

# initialization

email_nat = {}
with open('ilp/files/all_students.csv', 'r') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if i == 0: continue
        nationality = line[6].split("(")[0].strip()
        email_nat[line[7].lower().strip()] = nationality
        if nationality in nationality_data:
            nationality_data[nationality] += 1
        else: nationality_data[nationality] = 1
f.close()

# metro
with open("ilp/files/metro_icare.csv", 'r') as m:
    reader = csv.reader(m)
    for line in reader:
        site_name = line[1]
        site_cap = int(line[2])
        all_sites += [Site(site_name, site_cap)]
m.close()

# print(len(all_sites))

# provincial
with open("ilp/files/provincial_icare.csv", 'r') as p:
    reader = csv.reader(p)
    for line in reader:
        site_name = line[1]
        site_cap = int(line[2])
        all_sites += [Site(site_name, site_cap)]
p.close()

# print(len(all_sites))

# with open("ilp/files/real_icare.csv", 'r') as f:
with open("ilp/files/final2022.csv", 'r') as f:
    reader = csv.reader(f)
    
    for line_idx, line in enumerate(reader):
        if line_idx == 0:
            continue
        email = line[e_idx]
        name = line[n_idx[0]] + " " + line[n_idx[1]]

        previous = []
        pref_site_names = line[p_idx[0]:p_idx[1]]
        pref_sites = []
        for i in pref_site_names:
            for j in all_sites:
                if i == j.getName():
                    pref_sites += [j]
        grade = int(line[gr_idx].split()[1])
        gender = line[g_idx][0]

        if email.lower().strip() in email_nat:
            nationality = email_nat[email.lower().strip()]
        else: nationality = line[na_idx]

        total += 1

        cas_project, return_project = False, False

        if line[c_idx].lower() == "yes":
            cas_project = True
            total_cas_cnt += 1
        if line[r_idx] and line[r_idx].lower() == "yes":
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

while unassigned_students:
    for site in most_available(all_sites):
        weight, student = int(1e9), None
        for s in unassigned_students:
            temp_w = unassigned_other(nationality_data, site, s, grade_data, gender_data)
            if temp_w < weight:
                weight = temp_w
                student = s
        if student:
            site.add_student(student)
            student.setSite(site)
            unassigned_students.remove(student)

for site in most_available(all_sites):
    for pos_student in pos_allocations[site]:
        if pos_student not in site.getStudents() and not pos_student.senior_returning() and pos_student.isAssigned():
            assigned_site = pos_student.getSite()
            if (assigned_site.getLimit() - assigned_site.getTotal()) < (site.getLimit() - site.getTotal()):
                # talk to mr.woods about this section!!
                if not is_important(pos_student, assigned_site) and not too_frequent(pos_student, site):
                    assigned_site.remove_student(pos_student)
                    pos_student.setSite(site)
                    site.add_student(pos_student)

again_student = []

for site in all_sites:
    again_student += over_limit(site, nationality_data)

while again_student:
    for a in again_student:
        weight, site = int(1e9), None
        for s in availability(all_sites):
            temp_w = make_other(nationality_data, s, a, grade_data, gender_data)
            if temp_w < weight:
                weight = temp_w
                site = s
        site.add_student(a)
        a.setSite(site)
        again_student.remove(a)

# assign_students(availability(all_sites), again_student, nationality_data, grade_data, gender_data)

other_students, other_sites = impl_other(most_available(availability(all_sites)), all_students)
# change nationality_data & total_cas_cnt & total
print(len(availability(all_sites)), len(most_available(availability(all_sites))), "hi")

print(len(other_students), len(other_sites))

for site in other_sites:
    weight, student = int(1e9), None
    for s in other_students:
        temp_w = make_other(nationality_data, site, s, grade_data, gender_data)
        if temp_w < weight:
            weight = temp_w
            student = s
    if student:
        site.add_student(student)
        student.setSite(site)
        other_students.remove(student)

# just_check = LSA.run(other_students, other_sites, nationality_data, total_cas_cnt, total)

results = {}
check = []

for site in all_sites:
    students = site.getStudents()
    results[site.getName()] = students
    check += [site.getTotal()]

print(standard_deviation(check))

most_popular_site = least_popular(all_sites)[len(all_sites)-1]
least_popular_site = least_popular(all_sites)[0]
# pie(by_nationality(most_popular_site)[0], by_nationality(most_popular_site)[1])

# print(sum(check), "check")

for k, v in results.items():
    print(k, len(v))

# number of students who don't get one of their preferences (sorry but tis is the reality)
t = 0
p, m = 0, 0
for s in all_students:
    for i in s:
        site = i.getSite()
        if not site: print(i.getName())
        if site not in i.getPreferences():
            t += 1
        if i.want_provincial() and site.isMetro():
            p += 1
        if i.want_metro() and site.isProvincial():
            m += 1
            print(i.getName())
print(t, p, m)

toCSV(results)
toXLSX(results)

# by now all students should be assigned and it should be optimal!!