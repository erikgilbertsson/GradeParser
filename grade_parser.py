import pdfplumber
import re

FILE_NAME = "Intyg.pdf"
EXTRA_GRADES = [(5,7.5)]    # Add extra grades as tuples of (grade, scope)
USE_G = False		    # Use courses with U/G when averaging grade

def parse_row(row):
    scope_match = re.search(r' \d+,\dhp |\d+.\dhp', row)
    grade_match = re.search(r'\s\d\s|\s[GU]\s', row)
    if scope_match:
        scope = float(scope_match.group(0).split('hp')[0].replace(',', '.'))
        grade = 0
        if grade_match.group(0) == ' G ':
            if USE_G:
                grade = 3
            else:
                print("Skipped grade G.")
                return
        elif grade_match.group(0) != 'U':
            grade = int(grade_match.group(0))

        return (grade, scope)

def main():
    grades = []
    pdf = pdfplumber.open(FILE_NAME)
    for page in pdf.pages:
        page_str = page.extract_text().split('\n')
        for row in page_str:
            grade = parse_row(row)
            if grade:
                grades.append(grade)

    grades += EXTRA_GRADES
    total_weighted_grade = sum([grade[0] * grade[1] for grade in grades])
    total_scope = sum([grade[1] for grade in grades])
    print("Averaging " + str(len(grades)) + " grades. " + str(total_scope) + "hp.")
    print("Average grade: " + str(total_weighted_grade) + " / " + str(total_scope) + " = " + str(total_weighted_grade/total_scope))


if __name__ == "__main__":
    main()