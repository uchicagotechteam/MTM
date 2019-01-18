import chardet
import pandas as pd
import csv
from enum import Enum

tutors_column_names = {
#     name of the tutor
    "Name" : "Full Name",
#    email of the tutor  
    "Email" : "UChicago Email Address",
#     major of the tutor
    "Major" : "Intended Major (it's okay if you're Undecided!)",
#     the subjects the tutor is comfortable helping with (Comma separated)
    "Subjects" : 
    ["What subjects are you comfortable helping your student with?"],
#     the grades of the tutor is comfortable tutoring (Comma separated i.e. 5,6,7,8)
    "Grades" : "What grade levels are you comfortable tutoring? (please check all that apply)",
#     if tutor is an international student
    "International Student" : "Are you an international student? (We need this information to ensure you're paid directly by MTM, which keeps you from violating the terms of your visa.)",
#     if tutor has a disability
    "Disability" : "Are you comfortable working with students with disabilities including but not limited to autism, ADHD, and dyslexia? (Your honesty with this question helps us ensure that all students get a tutor who can fully address their needs.)",
#     if the tutor would be willing to do standardized test prep
    "Test Prep" : "Would you be willing to do standardized test prep for elementary schoolers within the one-on-one tutoring context? (We will provide the foundational resources for you.)",
#     the max number of students tutor is willing to take
    "Max Students" : "How many students would you like to take on? (Keep in mind that most families want to meet twice a week for 1-1.5 hours.)",
#     the availability of the tutor (expecting comma separated list of availability (i.e. Monday Evening, Tuesday Night))
    "Availability" : "What times are you available for tutoring? (check all that apply)",
#     work study
    "Work Study" : "Are you work study?",
#     if the tutor is already onboarded
    "Onboarded" : "Are you onboarded?",
}

class Tutor_Method(Enum):
    IN_PERSON = 1
    ONLINE_ONLY = 2
    NO_PREFERENCE = 3

guardians_column_names = {
    "First Name" : "Guardian First Name",
    "Last Name" : "Guardian Last Name",
    "Title" : "Guardian Preferred Title",
    "Email" : "Guardian Email Address",
    "Phone Number" : "Primary Phone Number",
    "Scholarship" : "Are you planning on applying for a scholarship?"
}

students_column_names = {
    "Disabled" : "Has your student been diagnosed with a learning disability and/or do they require special learning accommodations?",
    "First Name" : "First Name",
    "Last Name" : "Last Name",
    "Grade" : "Student Grade",
    "School" : "What school does your student attend?",
    "Subjects" : 
    [
    "What subjects does your student require tutoring in?", 
    "Math", 
    "Science", 
    "History/Social Science", 
    "English",
    "Foreign Language"
    ],
    "Frequency" : "How many times a week would you like to receive tutoring?",
    "Availability" : "When would you be available for tutoring?",
    "Previous Tutor" : "If you would like to continue to work with a previous tutor, what is their name (please include first and last, if possible)?"
}
class Tutor:

    def __init__(self, tutor_dict):
        '''
        Initialize every instance of Tutor with tutor_dict, a dictionary with one tutor's informtion.
        '''
#         Strings
        self.name = tutor_dict[tutors_column_names["Name"]]
 
        self.subjects = [];
        for col_name in tutors_column_names["Subjects"]:
            if tutor_dict[col_name] != 0:
                self.subjects.append(tutor_dict[col_name])

        self.major = tutor_dict[tutors_column_names["Major"]]
        self.email = tutor_dict[tutors_column_names["Email"]]
        
#         List
        self.grades = []
        self.parse_grades(tutor_dict)
        self.availability = [
            i.strip() for i in tutor_dict[tutors_column_names["Availability"]].split(',')]
    
#         Booleans
        self.intl_student = "yes" in tutor_dict[tutors_column_names["International Student"]].lower()
        self.disabl = "yes" in tutor_dict[tutors_column_names["Disability"]].lower()
        self.test_prep = "yes" in tutor_dict[tutors_column_names["Test Prep"]].lower()
           
#           Integers
        self.max_students = int(tutor_dict[tutors_column_names["Max Students"]])
        self.num_students = 0
        self.matched_students = []

        self.work_study = tutor_dict.get(tutors_column_names["Work Study"], False)
        self.onboarded = tutor_dict.get(tutors_column_names["Onboarded"], False)

    def parse_grades(self, tutor_dict):
        grades_responses = tutor_dict[tutors_column_names["Grades"]].split(',')
        if "Kindergarten - 2nd Grade" in self.grades:
            self.grades += list(range(0,3))
        if "3rd - 5th Grade" in self.grades:
            self.grades += list(range(3,6))
        if "6th - 8th Grade" in self.grades:
            self.grades += list(range(6,9))
        if "High School" in self.grades:
            self.grades += list(range(9,13))
    
    def __repr__(self):
        return f'Tutor({self.name})'

    def __str__(self):
        return f'Tutor({self.name})'

class Tutor_Manager:
    '''
    Tutor manager holds and initializes all instances of tutors from a given csv.
    '''
    def __init__(self, filename):
        self.tutors = []

        #open Tutors csv and turn each row into a Tutor instance
        with open(filename, 'r') as f1:
            reader = csv.DictReader(f1)
            for row in reader:
#                 if no email, skip
                if (row[tutors_column_names["Email"]] != ""):
                    tut = Tutor(row)
                    self.tutors.append(tut)

    def __repr__(self):
        return f'{self.tutors}'

    def __str__(self):
        return f'{self.tutors}'

class Guardian:

    def __init__(self, guardian_dict):
        '''
        Initialize Guardian object with guardian_dict, a dictionary with guardian info.
        '''
        self.first_name = guardian_dict[guardians_column_names["First Name"]]
        self.last_name = guardian_dict[guardians_column_names["Last Name"]]
        self.title = guardian_dict[guardians_column_names["Title"]]
        self.email = guardian_dict[guardians_column_names["Email"]]
        self.phone = guardian_dict[guardians_column_names["Phone Number"]]
        self.scholarship = guardian_dict[guardians_column_names["Scholarship"]]

    def __eq__(self, other):
        return (self.first_name == other.first_name) and (self.last_name == other.last_name)

    def __repr__(self):
        return f'Guardian({self.first_name} {self.last_name}, {self.email})'

    def __str__(self):
        return f'Guardian({self.first_name} {self.last_name}, {self.email})'
    
class Student:
    '''
    Every instance of Student represents one student. It requires that Tutor_Manager be run first.
    '''
    def __init__(self, student_dict, guardian, all_tutors):
        '''
        Iniitalize a student object.

        student_dict: dictionary with student information
        Guardian: Guardian object associated with student
        all_tutors: Tutor_Manager object with list of all tutors
        '''
        # print(student_dict)
        self.previous_tutor_match = None
        self.previous_tutor_name = None
        self.guardian = guardian
        self.disabl = False
        self.disabl = student_dict.get(students_column_names["Disabled"], "No") == "Yes"
        self.first_name = student_dict[students_column_names["First Name"]]
        self.last_name = student_dict[students_column_names["Last Name"]]
        self.grade = student_dict[students_column_names["Grade"]] #int
        self.grade = "".join([c for c in self.grade if str.isdigit(c)])

        self.school = student_dict[students_column_names["School"]]

        self.subjects = [];
        for col_name in students_column_names["Subjects"]:
            if student_dict[col_name] != 0:
                self.subjects.append(student_dict[col_name])

        self.frequency = student_dict[students_column_names["Frequency"]] 
        self.availability = []
        if student_dict[students_column_names["Availability"]] != 0:
            self.availability = [ i.strip() for i in student_dict[students_column_names["Availability"]].split(',')]
        if self.previous_tutor_name == 0:
            self.previous_tutor_name = None
        else:
            self.previous_tutor_name = student_dict[students_column_names["Previous Tutor"]]
            
        if self.previous_tutor_name: #student has a previous tutor preference, try to find a match within tutors list
            def find_previous_tutors(tutor_list):
                '''
                This method searches a list of all tutor objects to see if student's preferred previous tutor is within the list of current Tutor objects.
                If there are multiple matches, change self.check_previous_tutor to True.

                tutor_list: list of all Tutor objects

                returns: list of match(es) of Tutors (empty if no matches, 1 element if 1 match, multiple elements if more than 1 match)
                '''
#                 if not isinstance(self.previous_tutor_name, str): #self.previous_preference is 0
#                     raise TypeError
                match = []

                if len(self.previous_tutor_name.split()) == 1: #previous tutor name has one name, presumably a first 
                    match = [tutor 
                             for tutor in tutor_list.tutors 
                             if tutor.name.split()[0].upper().strip() == self.previous_tutor_name.upper().strip()
                            ] #split tutor name by space and compare first name to self.previous_tutor_name
#                     print(self)
#                     print(self.previous_tutor_name)
#                     print(match)
                else: #previous tutor name has more than one name, presumably a first and last
                    match = [tutor 
                             for tutor in tutor_list.tutors 
                             if tutor.name.upper() == self.previous_tutor_name.upper()
                            ]
#                     print(match)
                return match
            self.previous_tutor_match = find_previous_tutors(all_tutors) #all_tutors is the list of all tutors from Tutor_Manager

    def __repr__(self):
        str1 = "";
        str1 += " previous_tutor_match " + str(self.previous_tutor_match)
        str1 += "\n"
        str1 += " guardian " + str(self.guardian)
        str1 += "\n"
        str1 += " disabl " + str(self.disabl)
        str1 += "\n"
        str1 += " first_name " + str(self.first_name)
        str1 += "\n"
        str1 += " last_name " + str(self.last_name)
        str1 += "\n"
        str1 += " grade " + str(self.grade);
        str1 += "\n"
        str1 += " school " + str(self.school)
        str1 += "\n"
        str1 += " subjects " + str(self.subjects)
        str1 += "\n"
        str1 += " frequency " + str(self.frequency)
        str1 += "\n"
        str1 += " availability " + str(self.availability)
        str1 += "\n"
        str1 += " previous_tutor_name " + str(self.previous_tutor_name)
        str1 += "\n"
        return str1;
        # return f'Student({self.first_name}, {self.last_name})'

    def __str__(self):
        str1 = "";
        str1 += " previous_tutor_match " + str(self.previous_tutor_match)
        str1 += "\n"
        str1 += " guardian " + str(self.guardian)
        str1 += "\n"
        str1 += " disabl " + str(self.disabl)
        str1 += "\n"
        str1 += " first_name " + str(self.first_name)
        str1 += "\n"
        str1 += " last_name " + str(self.last_name)
        str1 += "\n"
        str1 += " grade " + str(self.grade);
        str1 += "\n"
        str1 += " school " + str(self.school)
        str1 += "\n"
        str1 += " subjects " + str(self.subjects)
        str1 += "\n"
        str1 += " frequency " + str(self.frequency)
        str1 += "\n"
        str1 += " availability " + str(self.availability)
        str1 += "\n"
        str1 += " previous_tutor_name " + str(self.previous_tutor_name)
        str1 += "\n"
        return str1;
        return f'Student({self.first_name}, {self.last_name})'

def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class Student_Manager:
    '''
    Student_Manager holds and initializes all instances of students from a given csv.
    '''
    def __init__(self, filename, all_tutors):
        '''
        Parse the csv file and initialize Student objects within the file.

        filename: csv with student info
        all_tutors: Tutor_Manager object with list of all tutors
        '''
        self.students = []
        self.guardians = []
        
        with open(filename, 'rb') as f:
            result = chardet.detect(f.read()) #identify encoding code needed for pandas read_csv
            
        student_dict = pd.read_csv(filename, encoding=result['encoding']) #create dataframe of csv 
        student_dict.fillna(0, inplace = True) 
        all_col_names = list(student_dict) #list of dataframe column names

        def add_students(df):
            '''
            This function takes the pandas dataframe generated from the csv file and parses it to
            find all students in the file.

            returns: list of Student objects
            '''
            students = []
            for i, row in df.iterrows(): 
                #row is a panda Series

                def guardian_info():
                    '''
                    Identify columns and values relating to the guardian of the student(s).

                    returns: dictionary with guardian-relevant keys and values
                    '''
                    guardian_dict = {} 
                    for col_name in all_col_names: 
                        if 'scholarship' in col_name.lower() or 'guardian' in col_name.lower() or 'phone' in col_name.lower(): #check for colnames with Guardian info 
                            guardian_dict[col_name] = row.get(col_name)
                    return guardian_dict

                #create Guardian of all student(s) in this row
                guardian_dict = guardian_info()
#                print(guardian_dict)
                if (guardian_dict == {}):
                    continue
                student_guardian = Guardian(guardian_dict) #create Guardian of all students in this row

                if student_guardian not in self.guardians:
                    self.guardians.append(student_guardian)
                
                #start parsing students
                for i in range(1, 3): #each row has max 4 students
                    name = f'Student {i} First Name'
                    # print('here 1')
                    student_i = df.columns.get_loc(name) #index of Student's first name
                    another_student_col = 'Do you have another student applying to MTM?' #column between students
                    
                    if i==1: #Student one
                        end_student_i = df.columns.get_loc(another_student_col) #Student one ends at first column that asks Do you have another student..?

                    elif i==2: #Student two
                        # print("about to crash\n")
                        if str(row.get(another_student_col)).upper() == 'YES' or row.get(name): #second student exists
                            next_student_col = another_student_col + f'.{i-1}'
                            end_student_i = df.columns.get_loc(next_student_col) #end of Student 2 ends with 'Do you have another student..?.1'
                        else:
                            break
                    
                    else: #Student three or four
                        # print("----------------------------------------")
                        # print(row.get(another_student_col + f'.{i-2}'))
                        if str(row.get(another_student_col + f'.{i-2}')).upper() == 'YES' or row.get(name):
                            next_student_col = another_student_col + f'.{i-1}'
                            end_student_i = df.columns.get_loc(next_student_col)
                        else:
                            break

                    student_dict = {}

                    #for each column in the range of the given student columns, add key and value to empty student_dict
                    for j in range(student_i, end_student_i):
                        col_name = df.columns[j] #find column name associated with column index
                        val = row.get(col_name) #get value in the row for that column name
                        
                        def trim_student_number(col_name):
                            trimmed_arr = col_name.split()
                            if len(trimmed_arr) >= 2:
                                if trimmed_arr[0].upper() == "Student".upper() and representsInt(trimmed_arr[1]):
                                    col_name = " ".join(trimmed_arr[2:])
                            trimmed_arr = col_name.split('.')
                            
                            if representsInt(trimmed_arr[-1]):
                                col_name = ".".join(trimmed_arr[:-1])
                                
                            return col_name
                        col_name = trim_student_number(col_name)
                        student_dict[col_name] = val #add column name as key and set value
#                        if len(col_name.split()) > 2 and col_name.split()[0].upper() == "Student".upper() and col_name.split()[1].upper() == "".upper() 
                    student_made = Student(student_dict, student_guardian, all_tutors)
                    #print(student_made)
                    students.append(student_made)
                    # print(student_made)
                    # print("made student\n")

            return students

        self.students = add_students(student_dict)

    def match_guardian(self, Guardian):
        '''
        This method takes a guardian name and finds all of the students associated with that guardian.

        guardian: Guardian object

        returns: list of student(s) with that guardian
        '''
        return [i 
                for i in self.students 
                if i.guardian == Guardian
               ]

    def __repr__(self):
        return f'{self.students}'

    def __str__(self):
        return f'{self.students}'

def main(filename1 = 'tutor.csv', filename2 = 'student.csv'):
    all_tutors = Tutor_Manager(filename1)
    all_students = Student_Manager(filename2, all_tutors)
    return all_tutors, all_students



# #Lauren Li
# #
# #MTM
# #
# #This file contains the implementation of Student, Tutor, Student_Manager, Tutor_Manager, and Guardian classes from specified csv files.

# import chardet
# import pandas as pd
# import csv

# class Tutor:

# 	def __init__(self, tutor_dict):
# 		'''
# 		Initialize every instance of Tutor with tutor_dict, a dictionary with one tutor's informtion.
# 		'''

# 		self.name = tutor_dict['Full Name'] #first and last name
# 		self.subjects = tutor_dict['What subjects are you comfortable helping yur student with?'] #subjects
# 		self.ap_tests = tutor_dict['If you answered yes to the previous question, which AP/IB tests are you comfortable tutoring?'] #AP Tests
# 		self.grades = tutor_dict['What grade levels are you comfortable tutoring? (please check all that apply)'].split(',')

# 		self.major = tutor_dict["Intended Major (it's okay if you're Undecided!)"] #Helps with assigning tutors to advanced subjects
# 		self.extra_subjects = tutor_dict['Please let us know if there are any other subjects you can help with (a foreign language, music theory, physics, chemistry, geometry, psychology, economics, British literature, etc.)']
		
# 		if tutor_dict["Are you an international student? (We need this information to ensure you're paid directly by MTM, which keeps you from violating the terms of your visa.)"] == 'Yes':
# 			self.intl_student = 1
# 		else:
# 			self.intl_student = 0

# 		if tutor_dict['Are you comfortable working with students with disabilities including but not limited to autism, ADHD, and dyslexia? (Your honesty with this question helps us ensure that all students get a tutor who can fully address their needs.)'] == 'Yes, I am comfortable with this although I have no experience tutoring students with disabilities.':
# 			self.disabl = 1
# 		else:
# 			self.disabl = 0

# 		if tutor_dict['Would you prefer to do in-person or online (i.e. via Skype, webwhiteboard, and other programs) tutoring?'] == 'In-person':
# 			self.tutor_method = 1
# 		elif tutor_dict['Would you prefer to do in-person or online (i.e. via Skype, webwhiteboard, and other programs) tutoring?'] == 'Either is fine':
# 			self.tutor_method = 0
# 		else: #online only
# 			self.tutor_method = -1

# 		if tutor_dict['Would you be willing to do standardized test prep for elementary schoolers within the one-on-one tutoring context? (We will provide the foundational resources for you.)'] == 'Yes':
# 			self.test_prep = 1
# 		else: #no test-prep
# 			self.test_prep = 0

# 		self.max_students = int(tutor_dict["How many students would you like to take on? (Keep in mind that most families want to meet twice a week for 1-1.5 hours.)"])
# 		self.num_students = 0
# 		self.matched_students = []

# 	def __repr__(self):
# 		return f'Tutor({self.name}), Matched students: {self.matched_students}'

# 	def __str__(self):
# 		return f'Tutor({self.name}), Matched students: {self.matched_students}'



# class Tutor_Manager:
# 	'''
# 	Tutor manager holds and initializes all instances of tutors from a given csv.
# 	'''
# 	def __init__(self, filename):
# 		self.tutors = []

# 		#open Tutors csv and turn each row into a Tutor instance
# 		with open(filename, 'r') as f1:
# 			reader = csv.DictReader(f1)
# 			for row in reader:
# 				tut = Tutor(row)
# 				self.tutors.append(tut)

# 	def __repr__(self):
# 		return f'{self.tutors}'
	
# 	def __str__(self):
# 		return f'{self.tutors}'



# class Guardian:

# 	def __init__(self, guardian_dict):
# 		'''
# 		Initialize Guardian object with guardian_dict, a dictionary with guardian info.
# 		'''
# 		self.first_name = guardian_dict['Guardian First Name']
# 		self.last_name = guardian_dict['Guardian Last Name']
# 		self.title = guardian_dict['Guardian Preferred Title']
# 		self.email = guardian_dict['Guardian Email Address']
# 		self.phone = guardian_dict['Primary Phone Number']
# 		self.scholarship = guardian_dict['Are you planning on applying for a scholarship?']

# 	def __eq__(self, other):
# 		return (self.first_name == other.first_name) and (self.last_name == other.last_name)

# 	def __repr__(self):
# 		return f'Guardian({self.first_name} {self.last_name}, {self.email})'

# 	def __str__(self):
# 		return f'Guardian({self.first_name} {self.last_name}, {self.email})'



# class Student:
# 	'''
# 	Every instance of Student represents one student. It requires that Tutor_Manager be run first.
# 	'''
# 	def __init__(self, student_dict, Guardian, all_tutors):
# 		'''
# 		Iniitalize a student object.

# 		student_dict: dictionary with student information
# 		Guardian: Guardian object associated with student
# 		all_tutors: Tutor_Manager object with list of all tutors
# 		'''

# 		for key in student_dict.keys():
# 			if 'FIRST NAME' in key.upper():
# 				self.first_name = student_dict[key]
# 			elif 'LAST NAME' in key.upper():
# 				self.last_name = student_dict[key]
# 			elif 'GRADE' in key.upper():
# 				self.grade = student_dict[key] #int
# 			elif 'SCHOOL' in key.upper():
# 				self.school = student_dict[key]
# 			elif 'SUBJECTS' in key.upper():
# 				self.subjects = student_dict[key]
# 			elif 'IN-PERSON OR ON-LINE' in key.upper():
# 				self.method = student_dict[key]
# 			elif 'TIMES A WEEK' in key.upper():
# 				self.frequency = student_dict[key] 
# 			elif 'AVAILABLE FOR TUTORING' in key.upper():
# 				self.availability = student_dict[key]
# 			elif 'PREVIOUS TUTOR' in key.upper():
# 				self.previous_tutor_name = student_dict[key] #if no preference, value should be 0
# 				self.check_previous_tutor = False #whether or not a human needs to check the student's previous tutor preference
# 				self.previous_tutor_match = [] #list of matches to current tutor list
# 			#elif 'MAROON TUTOR MATCH BEFORE' in key.upper():
# 				#self.return_student = student_dict[key]

# 		self.guardian = Guardian
# 		self.tutor_matches = []		

# 		if isinstance(self.previous_tutor_name, str): #student has a previous tutor preference, try to find a match within tutors list

# 			def find_previous_tutors(tutor_list):
# 				'''
# 				This method searches a list of all tutor objects to see if student's preferred previous tutor is within the list of current Tutor objects.
# 				If there are multiple matches, change self.check_previous_tutor to True.

# 				tutor_list: list of all Tutor objects

# 				returns: list of match(es) of Tutors (empty if no matches, 1 element if 1 match, multiple elements if more than 1 match)
# 				'''
# 				if not isinstance(self.previous_tutor_name, str): #self.previous_preference is 0
# 					raise TypeError

# 				match = []

# 				if len(self.previous_tutor_name.split()) == 1: #previous tutor name has one name, presumably a first 
# 					match = [tutor for tutor in tutor_list.tutors if tutor.name.split()[0].upper() == self.previous_tutor_name.upper()] #split tutor name by space and compare first name to self.previous_tutor_name
# 				else: #previous tutor name has more than one name, presumably a first and last
# 					match = [tutor for tutor in tutor_list.tutors if tutor.name.upper() == self.previous_tutor_name.upper()]

# 				if len(match) > 1:
# 					self.check_previous_tutor = True #there is more than one match so flag attribute as True to indicate that a human should check

# 				return match

# 			self.previous_tutor_match = find_previous_tutors(all_tutors) #all_tutors is the list of all tutors from Tutor_Manager				


# 	def __repr__(self):
# 		return f'Student({self.first_name}, {self.last_name})'
	
# 	def __str__(self):
# 		return f'Student({self.first_name}, {self.last_name})'



# class Student_Manager:
# 	'''
# 	Student_Manager holds and initializes all instances of students from a given csv.
# 	'''
# 	def __init__(self, filename, all_tutors):
# 		'''
# 		Parse the csv file and initialize Student objects within the file.

# 		filename: csv with student info
# 		all_tutors: Tutor_Manager object with list of all tutors
# 		'''
# 		self.students = []

# 		with open(filename, 'rb') as f:
# 			result = chardet.detect(f.read()) #identify encoding code needed for pandas read_csv
# 		student_dict = pd.read_csv(filename, encoding=result['encoding']) #create dataframe of csv 
# 		student_dict.fillna(0, inplace = True) 
# 		all_col_names = list(student_dict) #list of dataframe column names

# 		def add_students(df):
# 			'''
# 			This function takes the pandas dataframe generated from the csv file and parses it to
# 			find all students in the file.

# 			returns: list of Student objects
# 			'''
# 			students = []
# 			for i, row in df.iterrows(): 
# 				#row is a panda Series

# 				def guardian_info():
# 					'''
# 					Identify columns and values relating to the guardian of the student(s).

# 					returns: dictionary with guardian-relevant keys and values
# 					'''
# 					guardian_dict = {} 
# 					for col_name in all_col_names: 
# 						if 'scholarship' in col_name or 'Guardian' in col_name or 'Phone' in col_name: #check for colnames with Guardian info 
# 							guardian_dict[col_name] = row.get(col_name)
# 					return guardian_dict

# 				#create Guardian of all student(s) in this row
# 				guardian_dict = guardian_info()
# 				student_guardian = Guardian(guardian_dict) #create Guardian of all students in this row

# 				#start parsing students
# 				for i in range(1, 5): #each row has max 4 students
# 					name = f'Student {i} First Name'
# 					student_i = df.columns.get_loc(name) #index of Student's first name
# 					another_student_col = 'Do you have another student applying to MTM?' #column between students
# 					if i==1: #Student one
# 						end_student_i = df.columns.get_loc(another_student_col) #Student one ends at first column that asks Do you have another student..?
# 					elif i==2: #Student two
# 						if str(row.get(another_student_col)).upper() == 'YES' or row.get(name): #second student exists
# 							next_student_col = another_student_col + f'.{i-1}'
# 							end_student_i = df.columns.get_loc(next_student_col) #end of Student 2 ends with 'Do you have another student..?.1'
# 						else:
# 							break
# 					else: #Student three or four
# 						if str(row.get(another_student_col + f'.{i-2}')).upper() == 'YES' or row.get(name):
# 							next_student_col = another_student_col + f'.{i-1}'
# 							end_student_i = df.columns.get_loc(next_student_col)
# 						else:
# 							break

# 					student_dict = {}

# 					#for each column in the range of the given student columns, add key and value to empty student_dict
# 					for i in range(student_i, end_student_i):
# 						col_name = df.columns[i] #find column name associated with column index
# 						val = row.get(col_name) #get value in the row for that column name
# 						student_dict[col_name] = val #add column name as key and set value

# 					students.append(Student(student_dict, student_guardian, all_tutors))
					
# 			return students

# 		self.students = add_students(student_dict)

# 	def match_guardian(self, Guardian):
# 		'''
# 		This method takes a guardian name and finds all of the students associated with that guardian.

# 		guardian: Guardian object

# 		returns: list of student(s) with that guardian
# 		'''
# 		return [i for i in self.students if i.guardian == Guardian]


# 	def __repr__(self):
# 		return f'{self.students}'

# 	def __str__(self):
# 		return f'{self.students}'



# def main(filename1 = 'tutor.csv', filename2 = 'student.csv'):
# 	all_tutors = Tutor_Manager(filename1)
# 	all_students = Student_Manager(filename2)
    

'''        for key in student_dict.keys():
            if students_column_names["Disabled"].upper() in key.upper():
#                 CHECK THIS!
                self.disabl = student_dict[key] == "Yes"
            if 'FIRST NAME' in key.upper():
                self.first_name = student_dict[key]
            elif 'LAST NAME' in key.upper():
                self.last_name = student_dict[key]
            elif 'GRADE' in key.upper(): 
                self.grade = student_dict[key] #int
            elif 'SCHOOL' in key.upper():
                self.school = student_dict[key]
            elif 'SUBJECTS' in key.upper():
                self.subjects = student_dict[key]
            elif 'IN-PERSON OR ON-LINE' in key.upper():
                tutor_method_preference = student_dict[key]
                if tutor_method_preference == "In-person":
                    self.tutor_method = Tutor_Method.IN_PERSON
                elif tutor_method_preference == "Either is fine":
                    self.tutor_method = Tutor_Method.NO_PREFERENCE
                else:
                    self.tutor_method = Tutor_Method.ONLINE_ONLY
            elif 'TIMES A WEEK' in key.upper():
                self.frequency = student_dict[key] 
            elif 'AVAILABLE FOR TUTORING' in key.upper():
                if student_dict[key] == 0:
                    self.availability = []
                else:
                    self.availability = student_dict[key].split(',')
            elif 'PREVIOUS TUTOR' in key.upper():
                self.previous_tutor_name = student_dict[key] #if no preference, value should be 0

            #elif 'MAROON TUTOR MATCH BEFORE' in key.upper():
                #self.return_student = student_dict[key]
'''
