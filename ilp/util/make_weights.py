# calculating nationality ratio
def calc_nratio(snat, tnat):
    if tnat == 0: 
        return 0
    return snat/tnat

# calculating cas ratio
def calc_cratio(scas, tcas):
    if tcas == 0: return 0
    return scas/tcas

def make_weights(tnat, tcas, total, site, student):
    weight = 0
    pref_sites = student.getPreferences()

    if pref_sites:
        if site not in pref_sites:
            return 1e9

        if site.getTotal() >= 30:
            amt_weight = 100
        else: amt_weight = (site.getTotal()*100//total)
        weight += amt_weight

    if student.getPrevious():
        if site in student.getPrevious():
            weight += 10
    
    if student.getNationality():
        weight += int(calc_nratio(site.getSpecificNationality(student.getNationality()), tnat[student.getNationality()])*120)

    if student.is_planning_cas_project():
        weight += int(calc_cratio(site.getCasAmt(), tcas)*50) # make 20?
    
    if site.getGenders()[0] > site.getGenders()[1]:
        if student.getGender() == "M":
            weight += 10
    
    if site.getGenders()[0] < site.getGenders()[1]:
        if student.getGender() == "F":
            weight += 10
    
    if max(site.getGrades()) == student.getGrade()-9:
        weight += 15

    return weight