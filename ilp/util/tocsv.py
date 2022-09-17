import csv

def toCSV(results):
    with open('lip/files/result.csv', 'w') as f:
        f.truncate()
        writer = csv.writer(f)
        for k, v in results.items():
            for student in v:
                row = [k, student.getName(), student.getEmail(), str(student.getGrade()), student.getNationality(), student.getGender()]
                writer.writerow(row)

    f.close()