def availability(sites):
    result = []
    for site in sites:
        if site.has_space():
            result += [site]
    return result