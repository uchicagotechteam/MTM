from parse import *


main(filename = 'tutor.csv', filename2 = 'student.csv') # all_tutors + all_students



''' MUST-HAVE FUNCTIONS '''

# Checks if the tutor and student both have overlapping time availabilities

''' format -> ["day time"] 
			  ex: "Monday Evening" / "Friday Afternoon/Evening" / "Sunday Morning"
			  --- Morning / Afternoon / Evening '''

# Returns an integer --> number of overlapping day/time pairs

def time_match(tutor,student):


''' creating function to check if tutor and student comfortable match on disabilities'''
def disa_match(tutor, student):

	''' such that if student struggles with learning disabilities,
	 tutor will be comfortable with teaching'''

	 if student.disabl:
	 	if tutor.disabl: #if student has disability and tutor is comfortable
	 		return True
	 	else:
	 		return False # tutor is not comfortable
	 else:
	 	return False #student does not have learning disbility

''' international_match, if student is not scholarship student, checks to see if tutor is international
	If tutor international, student must be scholarship.
	If student not scholarship, tutor cannot be international '''
def international_match(tutor, student):

	if not student.scholarship:
		if tutor.intl_student:
			return False # internation cannot teach regular student
		else:
			return True
	else:
		return True # scholarship student can take any tutor



''' grade_subject_match is used if  student is in high school or need ACT/SAT prep.
	Purpose:
		1. If student needs standardized testing prep, tutor must be able to teach
		2. If high school student, tutor must be able to teach their specific subject, and 
			be comfortable with teaching high school student
				(ex. AP Chem, English, etc)
		3. If student it not in high school

'''
def grade_subject_match(tutor, student):

	# check if student is in high school
	if student.grade[0:2].isdigit():
		# check if tutor can teach high school
		for grade in tutor.grades:
			if(grade == "High School"):
				# check if their specific subjects match. (Kinda hard for math subjects)





				
		return False # if student is in high school and tutor cannot teach this grade range
	
	# check if ACT/SAT prep needed



''' must_have checks if student and tutor fulfill must-have requirements
	if not, tutor is removed from student list '''
def must_have(tutor, student):
	if international_match(tutor, student) &&
	   disa_match(tutor, student) &&
	   grade_subject_match(tutor, student) &&
	   time_match(tutor, student):
	   	return True # all must-haves match
	else:
		student.tutor_matches.remove(tutor)
		return False # some thing does not match

''' goes through list of students and remove tutors that do not fufill the must-have requirements
	from their list '''
def sort_must_have(student[]):





''' PREFERENCE FUNCTIONS '''

''' subject-match : Returns how many subjects the tutor can teach that overlaps with the student's needed subjects '''
'''
def subject_match(tutor,student):  # Returns integer -> How many subjects the tutor can teach 
	t = 0
	for subject-t in tutor.subjects:
		for subject-s in student.subjects:
			if subject-t == subject-s:
				t += 1
	return t 
	'''


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

	if student.grade == "K" or student.grade == "Pre-K":
		grade_student == 1

	else:

		if student.grade[0:2].isdigit():
			grade_student == 4  #High School

		elif student.grade[0].isdigit():

			grade_ == int(student.grade[0])

			if grade_ <= 2:
				grade_student == 1
			elif grade_ <= 5:
				grade_student == 2
			else:
				grade_student == 3

	for grade in grade_range:
		if grade_student == grade:
			match == True

	return match

''' based on matching preferences between student and tutor, return an integer
	weight.
	Three main preferences:
		1. If student requested a specific tutor
		2. If student and tutor subject matches (This is only a must-have if student in high school, otherwise, preference) 
'''
def preference_weight(tutor, student):
	return 0


''' function will leave tutor with highest preference weight in list
	this function should be called on the student with the least
	number of tutors first '''
def sort_preference(tutor, student):
	return 0

''' sort_students should sort students in list by lowest number of tutor in their
	object list to highest number '''
def sort_students(student[]):














