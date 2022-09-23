import xlsxwriter

def toXLSX(results):
    workbook = xlsxwriter.Workbook('ilp/files/result.xlsx')
    site_cnt = 1
    for k, v in results.items():
        row, col = 2, 0
        worksheet = workbook.add_worksheet("Site " + str(site_cnt))
        worksheet.write(0, 0, k)
        labels = ["Name", "Email", "Grade", "Nationality", "Gender"]
        label_col = 0
        for l in labels: 
            worksheet.write(1,label_col, l)
            label_col += 1
        
        male_students = []
        female_students = []
        other_students = []
        
        for s in v:
            if s.getGender() == "M": male_students += [s]
            elif s.getGender() == "F": female_students += [s]
            else: other_students += [s]
        
        male_data, female_data, other_data = [], [], []

        for m in male_students: male_data.append([m.getName(), m.getEmail(), m.getGrade(), m.getNationality(), "Male"])
        for f in female_students: female_data.append([f.getName(), f.getEmail(), f.getGrade(), f.getNationality(), "Female"])
        for o in other_students: other_data.append([o.getName(), o.getEmail(), o.getGrade(), o.getNationality(), "Other"])

        male_data.sort(key=lambda x: x[2])
        female_data.sort(key=lambda x: x[2])
        other_data.sort(key=lambda x: x[2])

        all = male_data + female_data + other_data

        for data in all:
            for d in data:
                worksheet.write(row, col, d)
                col += 1
            col = 0
            row += 1
        site_cnt += 1

    workbook.close()