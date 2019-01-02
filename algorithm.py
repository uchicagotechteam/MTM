from parse import *
from collections import defaultdict


#To-Do
# siblings


# Must-haves: 

'''	 Tutors should have at least two days of overlap with students 
     in their indicated availability 
	 I checked the Tutor class and there wasn't any attribute for availability (?) '''


''' subject-match : Returns how many subjects the tutor can teach that overlaps with the student's needed subjects '''
'''
def subject_match(tutor,student):
	
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

	subjects_ = [] # List of student subjects that are checked to see if they have overlap
	
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

	if "Math" in tutor.major:
		subjects_.extend(["Geometry","Trigonometry","Pre-Calculus","Calculus"]) # For advanced math subjects (older students)

	overlap = 0

	for student_subj in student.subjects.split(","):
		for tutor_subj in subjects_:
			if (student_subj == tutor_subj) or (student_subj in tutor.extra_subjects):
				overlap += 1

	return overlap 

'''

def subject_match(tutor, student):
        # Assumes dropdown/ checkboxes for subject
        # TODO : Advanced subjects 
        # basic subject matching
        return student.subject in tutor.subjects


''' grade-match : Returns 1 if student grade satisfies tutor's indicated grade range 
*** We're changing things to work with an easier to maintain google form'''

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


# Checks if tutor and student can both either meet in-person or online

def teach_method(tutor,student):
        if tutor.tutor_method == student.tutor_method:
                return 2
        elif (tutor.tutor_method == Tutor_Method.NO_PREFERENCE or
            student.tutor_method == Tutor_Method.NO_PREFERENCE):
                return 1
        return 0

def disability(tutor,student): #Must-have
	# Student disability status isn't indicated in the data given!!
	return (student.disabl and tutor.disabl) or not student.disabl

''' 
	Priority Order:
		1. Grade Level
		2. Subject
		3. Scholarship Status  '''
def must_have(tutor,student): # Checks must-haves (time-availability, disability, scholarship status)
	return time_match(tutor,student) >= 2) and inter_match(tutor,student) and disability(tutor,student)

def get_weight(tutor, student):                
	if not must_have(tutor,student):
                return 0
        return grade_match(tutor,student) * 10**3 + subject_match(tutor,student)*10**2 +/
time_match(tutor,student) * 10 + s.scholarship + teach_method(tutor,student)


def make_table():
        tutor_manager, student_manager = main()
        students = student_manager.students
        # sort so that 
        tutors = tutor_manager.tutors.sort(
                key = lambda k : k.work_study or k.onboarded)
	matched_table = defaultdict(list)
        for s in students:
                tutor = s.previous_tutor_match
                if not tutor or len(tutor) == 0:
                        continue
                if len(tutor) == 1:
                        matched_table[tutor] = s
                        students.remove(s)
                        tutor.max_students -= 1
                else:
                        # TODO : ask mtm about how to handle this case
                        print "Ambigious previous tutor for " + s + ". Please fix and rerun script."
        while(tutors and students):
                tutor = tutors.pop()
                # TODO siblings                
		best_student = max(students, lambda student: get_weight(tutor, student))
                matched_table[tutor].append(best_student)
                students.remove(best_student)
                tutor.max_students -= 1
                if tutor.max_students > 0:
                        tutors.append(tutor)                
        return matched_table


def get_matches():
        matches = make_table()
        print matches



	









			
# need a 'must-have' function that will check all 4 must-have conditions and then return true'
#Time: Tutors should also have at least 2 days of overlap with students in their indicated availability
# Disabilities
# International/scholarship 
# subject/grade-level (tutor must be comfortable if student is high school student, lower grades are just preference"

# We should eventually make a function that matches high school students' advanced subjects (esp STEM) to tutors with corresponding majors/skills













