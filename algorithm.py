from parse import *


main(filename = 'tutor.csv', filename2 = 'student.csv') # all_tutors + all_students

# I don't exactly know how to "pull" each student and tutor out of the managers to use in the functions(?)
# I'm getting an error that says the variables can't be assigned to their operators

# Must-haves: 

'''	 Tutors should have at least two days of overlap with students 
     in their indicated availability 
	 I checked the Tutor class and there wasn't any attribute for availability (?) '''


''' subject-match : Returns how many subjects the tutor can teach that overlaps with the student's needed subjects '''

def subject_match(tutor,student):  # Returns integer -> How many subjects the tutor can teach 
	t = 0
	for subject-t in tutor.subjects:
		for subject-s in student.subjects:
			if subject-t == subject-s:
				t += 1
	return t 



''' grade-match : Returns True if student is in the tutor's indicated grade range '''

def grade_match(tutor,student):  
	''' Kindergarten - 2nd
		3rd - 5th
		6th - 8th
		High School ''' # the grades for Tutor are separated by "," but still are strings
	grade_range = []

	# Assigning indicated grade intervals in tutor_dict to integer

	for grade in tutor.grades:
		if grade == "Kindergarten - 2nd Grade":
			grade_range.append(1)
		elif grade == "3rd - 5th Grade":
			grade_range.append(2)
		elif grade == "6th - 8th Grade":
			grade_range.append(3)
		else:  # High School
			grade_range.append(4)

	# Assigning student grade to integer based on tutor's ranges

	if student.grade == "Kindergarten" or student.grade <= 2:
		grade_student == 1
	elif student.grade <= 5:
		grade_student == 2
	elif student.grade <= 8:
		grade_student == 3
	else: 
		grade_student == 4

	match == False

	for grade in grade_range:
		if grade_student == grade:
			match == True

	return match 
			

















