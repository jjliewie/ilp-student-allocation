import numpy as np
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scipy.optimize import linear_sum_assignment
from util.make_weights import make_weights
from obj.site import Site

# linear sum assignment!
class LSA:
    def run(students, sites, nationality_data, total_cas_cnt, total):
        manual = []
        cost_matrix = []

        site_list = []

        ratio = len(students) // len(sites)
        remainder = len(students) % len(sites)

        for _ in range(ratio):
            site_list += sites
    
        unnamed_site = Site("X", int(1e9))
        for _ in range(remainder):
            site_list += [unnamed_site]

        for student in students:
            weights = []
            for site in site_list:
                if site.getName() == "X":
                    weight = 0
                else:
                    weight = make_weights(nationality_data, total_cas_cnt, total, site, student) # change later
                    # print("itsworking")
                weights += [weight]
            cost_matrix += [weights]
            # print(student.getName(), weights)

        cost_matrix = np.array(cost_matrix)

        _, col_ind = linear_sum_assignment(cost_matrix)
        opt_ass = col_ind
        # tc = cost_matrix[row_ind, col_ind].sum()

        opt_ass = list(opt_ass)
        # print(opt_ass)

        for i in range(len(students)):
            assigned_cost = cost_matrix[i, col_ind[i]]
            # print(assigned_cost)
            if assigned_cost >= 1e9:
                manual += [students[i]]
            elif opt_ass[i] >= len(students)-remainder:
                manual += [students[i]] 
            else:
                assignment = site_list[opt_ass[i]]
                assignment.add_student(students[i])
                students[i].setSite(assignment)
        
        return manual
