class Site:
    
    def __init__(self, name, limit):
        self.limit = limit
        self.name = name
        self.total_amt = 0
        self.students = []
        self.nationality_cntr = {}
        self.cas_amt = 0
        self.gender_cntr = [0, 0, 0]
        # male, female, other
        self.grade_cntr = [0, 0, 0, 0]
        # ninth, tenth, eleventh, twelfth
        self.specific_cntr = [
            [0, 0, 0], 
            [0, 0, 0], 
            [0, 0, 0], 
            [0, 0, 0]
        ]
    
    def getLimit(self):
        return self.limit
    
    def add_student(self, student):

        self.students += [student]

        self.grade_cntr[student.getGrade() - 9] += 1
        if student.getGender() == "M":
            self.gender_cntr[0] += 1
            self.specific_cntr[student.getGrade() - 9][0] += 1
        elif student.getGender() == "F":
            self.gender_cntr[1] += 1
            self.specific_cntr[student.getGrade() - 9][1] += 1
        else: 
            self.gender_cntr[2] += 1
            self.specific_cntr[student.getGrade() - 9][2] += 1

        if student.getNationality() in self.nationality_cntr.keys():
            self.nationality_cntr[student.getNationality()] += 1
        else: self.nationality_cntr[student.getNationality()] = 1

        if student.is_planning_cas_project():
            self.cas_amt += 1

        self.total_amt += 1
    
    def remove_student(self, student):

        if student not in self.students:
            return

        self.students.remove(student)
        self.grade_cntr[student.getGrade()-9] -= 1
        
        if student.getGender() == "M":
            self.gender_cntr[0] -= 1
            self.specific_cntr[student.getGrade() - 9][0] -= 1
        elif student.getGender() == "F":
            self.gender_cntr[1] -= 1
            self.specific_cntr[student.getGrade() - 9][1] -= 1
        else: 
            self.gender_cntr[2] -= 1
            self.specific_cntr[student.getGrade() - 9][2] -= 1

        self.nationality_cntr[student.getNationality()] -= 1

        if student.is_planning_cas_project():
            self.cas_amt -= 1

        self.total_amt -= 1

    def getGenders(self):
        return self.gender_cntr
    
    def getNationalities(self):
        return self.nationality_cntr
    
    def getSpecificNationality(self, x):
        if x in self.nationality_cntr:
            return self.nationality_cntr[x]
        return 0
    
    def getGrades(self):
        return self.grade_cntr
    
    def getCasAmt(self):
        return self.cas_amt
    
    def getName(self):
        return self.name
    
    def getStudents(self):
        return self.students
    
    def getTotal(self):
        return self.total_amt
    
    def isProvincial(self):
        if "(P)" in self.name:
            return True
        return False
    
    def isMetro(self):
        if "(M)" in self.name:
            return True
        return False
    
    def has_space(self):
        return self.total_amt < self.limit
    
    def getSpecific(self):
        return self.specific_cntr