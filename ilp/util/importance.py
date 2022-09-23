def is_important(student, site):
    genders = site.getGenders()
    grades = site.getGrades()

    gender = student.getGender()
    grade = student.getGrade()

    if gender == "M": gender_idx = 0
    else: gender_idx = 1

    if genders[gender_idx] < site.getTotal()//3:
        return True
    if grades[grade-9] < site.getTotal()//5:
        return True
    
    if site.getSpecific()[grade-9][gender_idx] <= 2:
        return True

    return False

def too_frequent(student, site):
    genders = site.getGenders()
    grades = site.getGrades()

    gender = student.getGender()
    grade = student.getGrade()

    if gender == "M": gender_idx = 0
    else: gender_idx = 1

    if genders[gender_idx] > (5 + site.getTotal()//2):
        return True
    if grades[grade-9] > (-2 +site.getTotal()//3):
        return True

    return False