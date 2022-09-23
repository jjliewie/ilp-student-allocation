import csv
from obj.student import Student
from util.rotation import rotation
from util.create_other_students import compile_others
from util.availability import availability
from util.popularity import most_available

e_idx, n_idx, g_idx, gr_idx = 7, [4, 1], 5, 0

def impl_other(pos_sites, students):
    left_sites = []
    left_students = compile_others(students)
    counter = len(left_students)
    l_sites = pos_sites

    for site_idx in range(len(l_sites)):
        if counter < 1: break
        if site_idx+1 == len(l_sites): diff = 0
        else: diff = l_sites[site_idx+1].getTotal() - l_sites[site_idx].getTotal()
        if diff == 0:
            left_sites += [l_sites[site_idx]]
            counter -= 1
            continue

        amt_in = (site_idx+1)*diff
        if amt_in <= counter:
            for _ in range(diff):
                left_sites += [l_sites[i] for i in range(site_idx+1)]
            counter -= amt_in
        else:
            left_sites += rotation(counter, l_sites[:site_idx+1])
            counter = 0
            break
    
    left_sites += rotation(counter, l_sites[:site_idx+1])
    
    other_site_dict = {}

    for i in left_sites:
        if i.getName() in other_site_dict:
            other_site_dict[i.getName()] += 1
        else: other_site_dict[i.getName()] = 1

    print(other_site_dict)
    
    return left_students, left_sites
