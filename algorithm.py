from parse import *
from collections import defaultdict

# Checks if there is any overlap between student and tutor subjects
def subject_match(tutor, student):
        return len(set(student.subject).intersection(set(tutor.subjects)))


''' 
grade-match : Returns 1 if student grade satisfies tutor's indicated grade range 
'''

def grade_match(tutor,student):  
        return student.grade in tutor.grades

# Checks if the tutor and student both have overlapping time availabilities

# Returns an integer --> number of overlapping day/time pairs

# Tutor class does not have availability element!!

def time_match(tutor,student):
        return sum ( s == t
                     for s in student.availability
                     for t in tutor.availability
        )


# Checks if a tutor is an international student
# An international tutor can only teach scholarship students

# There is no scholarship status for student data!!

def inter_match(tutor,student):
        return (tutor.intl_student and student.scholarship) or not tutor.intl_student

def disability(tutor,student): #Must-have
	# Student disability status isn't indicated in the data given!!
	return (student.disabl and tutor.disabl) or not student.disabl

''' 
	Priority Order:
		1. Grade Level
		2. Subject
		3. Scholarship Status  '''
# Checks must-haves (time-availability, disability, scholarship status)
def must_have(tutor,student):
	return (time_match(tutor,student) >= 2) and inter_match(tutor,student) and \
                disability(tutor,student)

def get_weight(tutor, student):               
    if (not must_have(tutor,student)):
        return 0
    else:
        return grade_match(tutor,student) * 10**3 + \
                subject_match(tutor,student)*10**2 + \
                time_match(tutor,student) * 10 + \
                s.scholarship 

def get_sibling_weight(tutor, siblings):
        if (tutor.max_students < len(siblings)):
                return 0
        weight = 0
        for student in siblings:
                if not (grade_match(tutor, student) and subject_match(tutor, student)):
                        return 0
                weight += get_weight(tutor, student)
        return weight

def match_family(tutor, siblings, matched_table, tutors, students):
        for student in siblings:
                matched_table[tutor].append(student)
                students.remove(student)
                tutor.max_students -= 1
        if tutor.max_students == 0:
                tutors.remove(tutor)

def make_table():
    tutor_manager, student_manager = main()
    students = student_manager.students
    # sort so that 
    tutor_manager.tutors.sort(
            key = lambda k : k.work_study or k.onboarded)
    tutors = tutor_manager.tutors
    families = [
            student_manager.match_guardian(g)
            for g in student_manager.guardians
    ]
    matched_table = defaultdict(list)
    # attempt to match siblings to the same tutor
    for family in families:
            if len(family) > 1:
                    best_tutor = max(tutors, key=lambda tutor: get_sibling_weight(tutor, family))
                    if (get_sibling_weight(best_tutor, family) != 0):
                            match_family(best_tutor, family, matched_table, tutors, students)

    to_remove = []

    for s in students:
            tutor = s.previous_tutor_match
            print(s)
            if not tutor or len(tutor) == 0:
                    continue
            if len(tutor) == 1:
                    tutor = tutor[0]
                    matched_table[tutor] = [s]
                    to_remove.append(s)
                    tutor.max_students -= 1
            else:
                    # TODO : ask mtm about how to handle this case
                    print("Ambigious previous tutor for " + s + ". Please fix and rerun script.")

    for student_to_remove in to_remove:
        students.remove(student_to_remove)

    while(tutors and students):
        tutor = tutors.pop()
            # TODO siblings                
        best_student = max(students, key=lambda student: get_weight(tutor, student))
        matched_table[tutor].append(best_student)
        students.remove(best_student)
        tutor.max_students -= 1
        if tutor.max_students > 0:
            tutors.append(tutor)
            
    return matched_table


def pairs_to_csv(matches):
    # tutor name, tutor email, guardian name, student name, guardian email
    csv_string = ""
    
    def append_item(i, csv_string):
        csv_string += empty_if_0(str(i)).replace(",", " & ") + ","
        return csv_string

    def finish_line(csv_string):
        csv_string += "\n"
        return csv_string
    
    def empty_if_0(i):
        return "" if i == 0 else i

# «Guardian_Email_Address»
# «Tutor_Email»
# «Guardian_Preferred_Title» 
# «Guardian_Last_Name»
# «Student_1_First_Name»
# «Student_Grade» «What_school_does_your_student_attend» «What_subjects_need_to_be_focused_on_Pl»
# «Tutor_First»
# «Student_2_First_Name»
# «Student_3_First_Name»
# «Student_4_First_Name»
# «Tutor_2_First»
# «Tutor_2_Email»
# «Scholarship_status_Scholarship_Pendin»

    csv_string = append_item("Guardian Email", csv_string)
    csv_string = append_item("Tutor Email", csv_string)
    csv_string = append_item("Guardian Preferred Title", csv_string)
    csv_string = append_item("Guardian Name", csv_string)
    csv_string = append_item("Student Name", csv_string)
    csv_string = append_item("Student Grade", csv_string)
    csv_string = append_item("School", csv_string)
    csv_string = append_item("Subjects", csv_string)
    csv_string = append_item("Tutor Name", csv_string)
    csv_string = append_item("Scholarship Status", csv_string)
    
    csv_string = finish_line(csv_string)
    
    for tutor, students in matches.items():
        for student in students:
            guardian = student.guardian
            csv_string = append_item(guardian.email, csv_string)
            csv_string = append_item(tutor.email, csv_string)
            csv_string = append_item(guardian.title, csv_string)
            csv_string = append_item(guardian.first_name + empty_if_0(guardian.last_name), csv_string)
            csv_string = append_item(student.first_name + empty_if_0(student.last_name), csv_string)
            csv_string = append_item(student.grade, csv_string)
            csv_string = append_item(student.school, csv_string)
            csv_string = append_item(student.subjects, csv_string)
            csv_string = append_item(tutor.name, csv_string)
            csv_string = append_item(guardian.scholarship, csv_string)
            csv_string = finish_line(csv_string)
    return csv_string        

def get_matches():
        matches = make_table()
        with open("output.csv", "w+") as file:
            csv_string = pairs_to_csv(matches)            
            file.write(csv_string)

get_matches()






			
# need a 'must-have' function that will check all 4 must-have conditions and then return true'
#Time: Tutors should also have at least 2 days of overlap with students in their indicated availability
# Disabilities
# International/scholarship 
# subject/grade-level (tutor must be comfortable if student is high school student, lower grades are just preference"

# We should eventually make a function that matches high school students' advanced subjects (esp STEM) to tutors with corresponding majors/skills













