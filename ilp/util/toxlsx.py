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
        for student in v:
            data = [student.getName(), student.getEmail(), student.getGrade(), student.getNationality(), student.getGender()]
            for d in data:
                worksheet.write(row, col, d)
                col += 1
            col = 0
            row += 1
        site_cnt += 1
    workbook.close()