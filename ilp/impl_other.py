import csv
from obj.student import Student
from util.rotation import rotation

def impl_other(all_sites_in_least):

    other_sites = []
    other_students = []

    with open("ilp/files/other_students.csv", 'r') as f:
        reader = csv.reader(f)
        other_amt = 0
        for line in reader:
            name = line[2] + " " + line[3]
            email = line[5]
            grade = int(line[0].split()[1])
            gender = line[1][0]
            nationality = line[4]
            other_amt += 1
            previous = []
            tmp_student = Student(email, [], nationality, 
            name, grade, gender, previous, False, False)
            other_students += [tmp_student]

        l_sites = all_sites_in_least

        counter = other_amt
        for site_idx in range(len(l_sites)-1):

            if counter < 1: break

            diff = l_sites[site_idx+1].getTotal() - l_sites[site_idx].getTotal()
            if diff == 0:
                other_sites += [l_sites[site_idx]]
                counter -= 1
                continue

            amt_in = (site_idx+1)*diff

            if amt_in <= counter:
                for _ in range(diff):
                    other_sites += [l_sites[i] for i in range(site_idx+1)]
                counter -= amt_in
            else:
                other_sites += rotation(counter, l_sites[:site_idx+1])
                break

    f.close()

    other_site_dict = {}

    for i in other_sites:
        if i in other_site_dict:
            other_site_dict[i] += 1
        else: other_site_dict[i] = 1
    return other_students, other_sites
