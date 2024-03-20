
import csv
from datetime import datetime


class Student:
    def __init__(self, student_id, last_name, first_name, major, disciplinary_action=None):
        self.student_id = student_id
        self.last_name = last_name
        self.first_name = first_name
        self.major = major
        self.disciplinary_action = disciplinary_action


class GPA:
    def __init__(self, student_id, gpa):
        self.student_id = student_id
        self.gpa = float(gpa)


class GraduationDate:
    def __init__(self, student_id, graduation_date):
        self.student_id = student_id
        self.graduation_date = datetime.strptime(graduation_date, '%m/%d/%Y')


# Step 1: Read data from CSV files and create objects
students = {}
with open('StudentsMajorsList.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        student_id, last_name, first_name, major, disciplinary_action = row
        students[student_id] = Student(student_id, last_name, first_name, major, disciplinary_action)

gpas = {}
with open('GPAList.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        student_id, gpa = row
        gpas[student_id] = GPA(student_id, gpa)

graduation_dates = {}
with open('GraduationDatesList.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        student_id, graduation_date = row
        graduation_dates[student_id] = GraduationDate(student_id, graduation_date)

# Step 2: Process data and create required reports
full_roster = []
major_reports = {}
scholarship_candidates = []
disciplined_students = []


# Helper function for sorting by last name
def sort_by_last_name(item):
    return item[3]


# Helper function for sorting by student ID
def sort_by_student_id(item):
    return item[0]


# Helper function for sorting by GPA
def sort_by_gpa(item):
    return item[4]


# Helper function for sorting by graduation date
def sort_by_graduation_date(item):
    return datetime.strptime(item[3], '%m/%d/%Y')



def is_valid_student(student_id):
  return student_id in students and student_id in graduation_dates and not students[student_id].disciplinary_action


for student_id, student in students.items():
    gpa = gpas.get(student_id)
    graduation_date = graduation_dates.get(student_id)

    if gpa and graduation_date:
        # a. FullRoster.csv
        full_roster.append([student_id, student.major, student.first_name, student.last_name,
                            gpa.gpa, graduation_date.graduation_date.strftime('%m/%d/%Y'), student.disciplinary_action])

        # b. List per major
        major_file_name = f'{student.major.replace(" ", "")}Students.csv'
        if student.major not in major_reports:
            major_reports[student.major] = []
        major_reports[student.major].append([student_id, student.last_name, student.first_name,
                                             graduation_date.graduation_date.strftime('%m/%d/%Y'),
                                             student.disciplinary_action])

        # c. ScholarshipCandidates.csv
        if float(gpa.gpa) > 3.8 and student.disciplinary_action != 'Y':
            scholarship_candidates.append([student_id, student.last_name, student.first_name,
                                           student.major, gpa.gpa])

        # d. DisciplinedStudents.csv
        if student.disciplinary_action:
            disciplined_students.append([student_id, student.last_name, student.first_name,
                                         graduation_date.graduation_date.strftime('%m/%d/%Y')])

# Sort the reports
full_roster.sort(key=sort_by_last_name)  # Sort by last name
for major, report in major_reports.items():
    report.sort(key=sort_by_student_id)  # Sort by student ID
scholarship_candidates.sort(key=sort_by_gpa, reverse=True)  # Sort by GPA
disciplined_students.sort(key=sort_by_graduation_date)  # Sort by graduation date

# Find the unique disciplined students based on student ID
unique_disciplined_students = []
seen_student_ids = set()

for student in disciplined_students:
    if student[0] not in seen_student_ids:
        unique_disciplined_students.append(student)
        seen_student_ids.add(student[0])

# Interactive Query Capability
while True:
    # Get user input for major and GPA
    query = input("Enter major and GPA (e.g., 'Computer Science 3.5', or 'q' to quit): ")

    # Check if the user wants to quit
    if query.lower() == 'q':
        break

    # Split user input into major and GPA
    input_parts = query.rsplit(' ', 1)

    if len(input_parts) != 2:
        print("Invalid input. Please enter both major and GPA separated by a space.")
        continue

    major, gpa_input = input_parts

    try:
        # Convert GPA input to float
        target_gpa = float(gpa_input)
    except ValueError:
        print("Invalid GPA. Please enter a valid GPA.")
        continue

    # Find students matching the query
    matching_students = []

    for student_id, student in students.items():
        if student.major == major and is_valid_student(student_id):
            gpa = gpas.get(student_id)
            if gpa and abs(gpa.gpa - target_gpa) <= 0.1:
                matching_students.append([student_id, student.first_name, student.last_name, gpa.gpa])

    if not matching_students:
        # If no students within 0.1 GPA, try finding within 0.25 GPA
        for student_id, student in students.items():
            if student.major == major and is_valid_student(student_id):
                gpa = gpas.get(student_id)
                if gpa and abs(gpa.gpa - target_gpa) <= 0.25:
                    matching_students.append([student_id, student.first_name, student.last_name, gpa.gpa])

    if not matching_students:
        # If still no matches, find the closest GPA within the major
        closest_student = None
        min_gpa_difference = float('inf')

        for student_id, student in students.items():
            if student.major == major and is_valid_student(student_id):
                gpa = gpas.get(student_id)
                if gpa:
                    gpa_difference = abs(gpa.gpa - target_gpa)
                    if gpa_difference < min_gpa_difference:
                        closest_student = [student_id, student.first_name, student.last_name, gpa.gpa]
                        min_gpa_difference = gpa_difference

        if closest_student:
            matching_students.append(closest_student)

    # Display the results
    if matching_students:
        print("Your student(s):")
        for student_info in matching_students:
            print(f"  {student_info[0]}, {student_info[1]} {student_info[2]}, GPA: {student_info[3]}")
    else:
        print("No such student")

    # Query the user again
    print()  # Add a newline for better formatting


# Step 3: Write reports to CSV files
with open('FullRoster.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(full_roster)

for major, report in major_reports.items():
    with open(f'{major}Students.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(report)

with open('ScholarshipCandidates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(scholarship_candidates)

with open('DisciplinedStudents.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write rows without the header
    writer.writerows(unique_disciplined_students)

print()
