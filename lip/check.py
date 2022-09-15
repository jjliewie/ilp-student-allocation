import csv
all_site_names = []
with open("lip/files/real_icare.csv", 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        for i in list(line)[1:5]:
            if i not in all_site_names:
                all_site_names += [i]
f.close()

all_site_names.sort()

provincial, metro = [], []

for i in all_site_names:
    if "(P)" in i:
        provincial += [i]
    else: metro += [i]

with open("lip/files/check_sites.csv", 'w') as f:
    f.truncate()
    writer = csv.writer(f)
    for i in provincial:
        row = [i]
        writer.writerow(row)
    for i in metro:
        row = [i]
        writer.writerow(row)
f.close()