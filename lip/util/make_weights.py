# calculating nationality ratio
def calc_nratio(snat, tnat):
    if tnat == 0: 
        print("shit")
        return 0
    return snat/tnat

# calculating cas ratio
def calc_cratio(scas, tcas):
    if tcas == 0: return 0
    return scas/tcas

def make_weights(tnat, tcas, total, site, student):
    weight = 0
    pref_sites = student.getPreferences()
    if site in pref_sites:
        idx = pref_sites.index(site)
    else: return 1e9

    weight += 10*idx

    if site.getTotal() >= 30:
        amt_weight = 1000
    else: amt_weight = (site.getTotal()*100//total)
    weight += amt_weight
    # print("weights: ", site.getTotal(), site.getName(), amt_weight)

    if student.getPrevious():
        if site in student.getPrevious():
            weight += 10
    
    weight += int(calc_nratio(site.getSpecificNationality(student.getNationality()), tnat[student.getNationality()])*20)
    weight += int(calc_cratio(site.getCasAmt(), tcas)*20) # make 20?

    return weight