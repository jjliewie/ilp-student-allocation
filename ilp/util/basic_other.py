def make_other(tnat, site, student, tgrade, tgender):
    weight = 0

    if site not in student.getPreferences():
        weight += 1000

    if student.getNationality():
        weight += int((site.getSpecificNationality(student.getNationality())/tnat[student.getNationality()])*40)

    if student.getPrevious():
        if site in student.getPrevious():
            weight += 10

    site_genders = site.getGenders()
    site_grades = site.getGrades()

    site_grade_ratio = site_grades[student.getGrade()-9] / sum(site_grades)
    total_grade_ratio = tgrade[student.getGrade()-9] / sum(tgrade)

    if site_grade_ratio > total_grade_ratio:
        weight += int(500*(site_grade_ratio-total_grade_ratio))
    else: weight -= 10

    # other gender population at ISM is quite small
    if student.getGender() == "M": idx = 0
    else: idx = 1

    site_gender_ratio = site_genders[idx] / sum(site_genders)
    total_gender_ratio = tgender[idx] / sum(tgender)

    if site_gender_ratio > total_gender_ratio:
        weight += int(500*(site_gender_ratio-total_gender_ratio))
    else: weight -= 10

    weight -= (site.getTotal()-site.getLimit())*80

    specific = site.getSpecific()
    if specific[student.getGrade()-9][idx]/site.getTotal() > 0.2:
        weight += 50
    
    if student.want_provincial() and site.isMetro():
        weight += 1000
    if student.want_metro() and site.isProvincial():
        weight += int(1e9)

    return weight

def unassigned_other(tnat, site, student, tgrade, tgender):
    weight = 0

    if site not in student.getPreferences():
        return int(1e9)

    if student.getNationality():
        weight += int((site.getSpecificNationality(student.getNationality())/tnat[student.getNationality()])*40)

    if student.getPrevious():
        if site in student.getPrevious():
            weight += 10

    site_genders = site.getGenders()
    site_grades = site.getGrades()

    site_grade_ratio = site_grades[student.getGrade()-9] / sum(site_grades)
    total_grade_ratio = tgrade[student.getGrade()-9] / sum(tgrade)

    if site_grade_ratio > total_grade_ratio:
        weight += int(400*(site_grade_ratio-total_grade_ratio))
    else: weight -= 10

    # other gender population at ISM is quite small
    if student.getGender() == "M": idx = 0
    else: idx = 1

    site_gender_ratio = site_genders[idx] / sum(site_genders)
    total_gender_ratio = tgender[idx] / sum(tgender)

    if site_gender_ratio > total_gender_ratio:
        weight += int(400*(site_gender_ratio-total_gender_ratio))
    else: weight -= 10

    weight -= (site.getTotal()-site.getLimit())*80

    specific = site.getSpecific()
    if specific[student.getGrade()-9][idx]/site.getTotal() > 0.2:
        weight += 50
    else: weight -= 10

    return weight