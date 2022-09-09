# import csv

# # open the file in the write mode
# f = open('path/to/csv_file', 'w')

# # create the csv writer
# writer = csv.writer(f)

# # write a row to the csv file
# writer.writerow(row)

# # close the file
# f.close()

from obj.student import Student
from obj.site import Site
from algo.lsa import LSA

unassigned_students = []

si1 = Site("gawad")
si2 = Site("Hellow")
si3 = Site("Nihao")

st1 = Student('as', [si1, si2, si3], "jijs", "julie", 12, "f", [], False, False)
st2 = Student('as', [si2], "jijs", "julie1", 12, "f", [], False, False)
st3 = Student('as', [si2], "jijs", "julie2", 12, "f", [], False, False)
st4 = Student('as', [si2], "jijs", "stela", 12, "f", [], False, False)
# st5 = Student('as', [si2], "jijs", "sohpi", 12, "f", [], False, False)

sts = [st1, st2, st3, st4]
sis = [si1, si2, si3]

unassigned_students += LSA.run(sts, sis, {"jijs":4}, 1000)

# after everything

for us in unassigned_students:
    print(us.getName())

print(si1.getTotal())
print(len(si1.getStudents()))

# from docs

# import numpy as np
# from scipy.optimize import linear_sum_assignment

# cost_matrix = np.array([
#     [0, 1, 2], 
#     [0, 2, 1], 
#     [1, 0, 2]
# ])

# row_ind, col_ind = linear_sum_assignment(cost_matrix)
# opt_ass = col_ind
# tc = cost_matrix[row_ind, col_ind].sum()
# for i in range(3):
#     print(cost_matrix[i, col_ind[i]])

# print(opt_ass)
# print('Total Assignment cost is %d' %tc)
