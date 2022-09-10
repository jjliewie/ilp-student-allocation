class Student:

    def __init__(self, email, preferences, nationality, name, 
    grade, gender, previous, cas_project, return_project):

        self.preferences = preferences
        self.nationality = nationality
        self.name = name
        self.email = email
        self.grade = grade
        self.gender = gender
        self.previous = previous
        self.cas_project = cas_project
        self.return_project = return_project

        self.assigned_site = None

    # def is_assigned(self):
    #     if self.assigned_site: return True
    #     return False
    
    # def assign(self, site):
    #     self.assigned_site = site

    def setSite(self, site):
        self.assigned_site = site

    def getSite(self):
        return self.assigned_site

    def getPreferences(self):
        return self.preferences
    
    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def getGender(self):
        return self.gender
    
    def getGrade(self):
        return self.grade
    
    def getNationality(self):
        return self.nationality

    def senior_returning(self):
        return self.return_project

    def is_planning_cas_project(self):
        return self.cas_project
    
    def getPrevious(self):
        return self.previous

# debugging

# p1 = Student('as', [1, 2, 3], "jijs", "dh", 12, "f", [], False, False)
# p1.setPreferences([3, 4, 1])
# print(p1.is_assigned())
# p1.assign("gawad")
# print(p1.is_assigned())