def least_popular(sites):
    site_info = []
    for i in range(len(sites)):
        site_info.append([sites[i].getTotal(), i])
    site_info.sort()
    least = []
    for i in range(len(sites)):
        least += [sites[site_info[i][1]]]
    # for i in least:
    #     print(i.getName())
    return least

# lol i actually didn't need this but i'm keeping it because I like the code
# and I might need it when I am refactoring
def pop_counter(sites):
    pop_dict = {}
    current = least_popular(sites)
    for i, site in enumerate(current):
        pop_dict[site] = i
    return pop_dict