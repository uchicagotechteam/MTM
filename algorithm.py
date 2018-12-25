from parse import *


main(filename = 'tutor.csv', filename2 = 'student.csv') # all_tutors + all_students

# Must-haves: 

'''	 Tutors should have at least two days of overlap with students 
     in their indicated availability 
	 I checked the Tutor class and there wasn't any attribute for availability (?) '''


''' subject-match : Returns how many subjects the tutor can teach that overlaps with the student's needed subjects '''



def subject_match(tutor,student):  # Returns integer -> How many subjects the tutor can teach 
	
	'''
	Reading

	Math 		//		Geometry, Trigonometry, Calculus, Pre-Calculus
						(have these options)

	Science		//		Chemistry, Biology, Physics, CS

	English		//		AP English
	History (U.S.)		// AP World History

	Study/Organizational Skills == Study

	Misc 		//		French, CPS Testing, Spanish, Test-Prep, College Algebra, Japanese
				//		"Will discuss", SAT/ACT Prep

				(please make this a bullet)
	

	All (will combine core subjects listed above-left)
	'''

	# COVERING BASIC SUBJECTS (options listed for tutors)

	subjects_ = []
	
	for subject in tutor.subjects.split(","):

		if "Reading Comprehension" in subject:
			subjects_.append("Reading")

		elif "Basic Math" in subject:
			subjects_.append("Math")  # basic math up unti 8th grade-ish

		elif "English" in subject:
			subjects_.append("English")

		elif "General Science" in subject:
			subjects_.append("Science")

		elif "U.S. History" in subject:
			subjects_.append("History")  # assuming this will cover basic, elementary-school history topics 

		else:  #Study/Organizational Skills
			subjects_.append("Study")

''' grade-match : Returns 1 if student grade satisfies tutor's indicated grade range '''

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
			elif grade <= 8:
				grade_student == 3
			else:
				grade_student == 4   # Case for 9th graders

	for grade in grade_range:
		if grade == grade_student:
			return 1

	return 0





# Checks if the tutor and student both have overlapping time availabilities

# Returns an integer --> number of overlapping day/time pairs

# Tutor class does not have availability element!!

def time_match(tutor,student):

	tutor_avail = tutor.availability
	t_avail = tutor_avail.title() #letters in spreadsheet are lowercase

	student_avail = student.availability

	overlap == 0

	for s in student_avail.split(","):
		for t in t_avail.split(","):
			if s == t:
				overlap += 1

	return overlap

	# what if a student only wants one day of tutoring? (per week)



# Checks if a tutor is an international student
# An international tutor can only teach scholarship students

# There is no scholarship status for student data!!

def inter_match(tutor,student):

	if tutor.intl_student == 1:

		if student.scholarship == 1:   # student.scholarship is not an existing element (just made up)
			return 1 
		else:
			return 0

	else:
		return 1

		# 1 --> tutor and student can be paired

		# 0 --> tutor and student cannot be paired


# Checks if tutor and student can both either meet in-person or online

def teach_method(tutor,student):

	if student.method == "In-person":
		method = 1

	elif student.method == "Either is fine":
		method = 0

	else: #online
		method = -1

	if tutor.tutor_method == method: # 2 means tutor and student have same preferences
		return 2					 #      (ex: On-line / On-line)

	elif tutor.tutor_method == 0:    # Tutor is fine with both in-person and on-line
		return 1

	else:                            # Tutor and Student have conflicting preferences
		return 0


def disability(tutor,student): #Must-have

	# Student disability status isn't indicated in the data given!!

	if student.disabl == 1:  # student.disabl non-existent
		if tutor.disabl == 1:
			return 1
		else: 
			return 0

	else:
		return 1

		# 1 --> tutor and student can be paired

		# 0 --> tutor and student cannot be paired




	









			
# need a 'must-have' function that will check all 4 must-have conditions and then return true'
#Time: Tutors should also have at least 2 days of overlap with students in their indicated availability
# Disabilities
# International/scholarship 
# subject/grade-level (tutor must be comfortable if student is high school student, lower grades are just preference"

# We should eventually make a function that matches high school students' advanced subjects (esp STEM) to tutors with corresponding majors/skills













