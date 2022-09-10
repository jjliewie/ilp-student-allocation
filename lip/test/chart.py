import matplotlib.pyplot as plt
import numpy as np

def by_amt(sites):
    dataset = {}
    for site in sites:
        dataset[site.getName()] = site.getTotal()
    return dataset

def by_nationality(site):
    nationalities = site.getNationalities()
    values, labels = [], []
    for l, v in nationalities.items():
        values.append(v)
        labels.append(l)
    return values, labels

def by_grade(site):
    grades = site.getGrades()
    labels = ["Grade 9", "Grade 10", "Grade 11", "Grade 12"]
    return grades, labels

def by_gender(site):
    genders = site.getGenders()
    labels = ["Male", "Female", "Other"]
    # print(genders)
    return genders, labels

def pie(values, my_labels):
    plt.pie(np.array(values), labels = my_labels)
    plt.show()

def bar(data, x="", y="", title=""):
    labels = list(data.keys())
    values = list(data.values())
    fig = plt.figure(figsize = (10, 5))
    plt.bar(labels, values, color ='maroon',
        width = 0.4)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.show()
    