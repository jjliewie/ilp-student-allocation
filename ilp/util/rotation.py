def rotation(cnt, sites):
    result = []
    for i in range(0, cnt):
        if i < len(sites):
            result += [sites[i]]
        else:
            result += [sites[i % len(sites)]]
    return result