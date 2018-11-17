'''
MTM

1. Work on schema for Student, Tutor, and maybe Guardian objects?
2. What attributes?
3. What methods?
4. 

Read csv -> parse through to create all objects -> pass objects to user

Student class attributes
first name #often combined with last name 
check:
1. is there a value in "last name"
2. if not, are there multiple names in first name
3. take last one in first and put it as last name 
last name -> check if field is empty
guardian -> combine first and last?
grade - need to have a key to get it all to K-12 as strings
age
subjects
school
times available
times per week
contact info
preferred tutor first
preferred tutor last
special info



Tutor class attributes
first
last
subjects
preferred location
availability

'''

import pandas as pd
import chardet

class Guardian:
	def __init__(self, guardian_dict):
		self.first_name = guardian_dict['Guardian First Name']
		self.last_name = guardian_dict['Guardian Last Name']
		self.title = guardian_dict['Guardian Preferred Title']
		self.email = guardian_dict['Guardian Email Address']
		self.phone = guardian_dict['Primary Phone Number']
		self.scholarship = guardian_dict['Are you planning on applying for a scholarship?']

	def __repr__(self):
		return f'Guardian({self.first_name} {self.last_name}, {self.email})'

class Student:
	def __init__(self, student_dict, Guardian):
		for key in student_dict.keys():
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
				self.method = student_dict[key]
			elif 'TIMES A WEEK' in key.upper():
				self.frequency = student_dict[key] 
			elif 'AVAILABLE FOR TUTORING' in key.upper():
				self.availability = student_dict[key]
			elif 'PREVIOUS TUTOR' in key.upper():
				self.previous_preference = student_dict[key]
			elif 'MAROON TUTOR MATCH BEFORE' in key.upper():
				self.return_student = student_dict[key]

		self.guardian = Guardian

	def __repr__(self):
		return f'Student'



class Student_Manager:

	def __init__(self, filename):
		self.students = []

		with open(filename, 'rb') as f:
			result = chardet.detect(f.read()) #identify encoding code needed for pandas read_csv
		student_dict = pd.read_csv(filename, encoding=result['encoding'])
		student_dict.fillna(0)
		all_col_names = list(student_dict) #list of dataframe column names
		#student_dict = student_dict.to_dict(orient='records')

		def add_students(df):
			students = []
			for i, row in df.iterrows(): #row is a panda Series
				#row = row.to_frame().transpose() #change series into its own dataframe with column names

				def guardian_info():
					guardian_dict = {} 
					for col_name in all_col_names: 
						if 'scholarship' in col_name or 'Guardian' in col_name or 'Phone' in col_name: #check for colnames with Guardian info 
							guardian_dict[col_name] = row.get(col_name)
					return guardian_dict

				guardian_dict = guardian_info()
				student_guardian = Guardian(guardian_dict) #create Guardian of all students in this row

				#start parsing students
				for i in range(1, 5): #each row has max 4 students
					name = f'Student {i} First Name'
					another_student_col = 'Do you have another student applying to MTM?' #column between students
					if i==1:
						student_i = df.columns.get_loc(name) #index of student 1 First name
						end_student_i = df.columns.get_loc(another_student_col) #index 21
						student_one_dict = {}
						for i in range(student_i, end_student_i):
							col_name = df.columns[i]
							val = row.get(col_name)
							student_one_dict[col_name] = val
							#student_one_dict = dict(row.iloc[:, :col_i])
						students.append(Student(student_one_dict, student_guardian))
					elif i == 2: #student 2
						if row.get(another_student_col) or row.get(name): #second student exists
							student_two_i = df.columns.get_loc(name) #index of Student 2 First Name
							next_student_col = another_student_col + f'.{i-1}'
							end_student_two_i = df.columns.get_loc(next_student_col) #index of "Do you have another...?.1"
							student_dict = {}
							for i in range(student_two_i, end_student_two_i):
								col_name = df.columns[i]
								val = row.get(col_name)
								student_dict[col_name] = val
							students.append(Student(student_dict, student_guardian))
						else:
							break
					else: #student 3 or 4
						if row.get(next_student_col) or row.get(name): #third or fourth student exists
							student_i = df.columns.get_loc(name) #index of Student 3  or 4 First Name
							next_student_col = another_student_col + f'.{i-2}' #resetting to find next Do you have another...? column
							end_student_i = df.columns.get_loc(next_student_col) #index of "Do you have another...?.2 or .3"
							student_dict = {}
							for i in range(student_i, end_student_i):
								col_name = df.columns[i]
								val = row.get(col_name)
								student_dict[col_name] = val
							students.append(Student(student_dict, student_guardian))
						else:
							break
			return students

		self.students = add_students(student_dict)

	def __repr__(self):
		return f'{self.students}'


'''
def guardian_info(df):
	guardian_col_name = []
	guardian_data = []
	student_dict_col = list(df)
	for col_name in student_dict_col:
		if 'scholarship' in col_name or 'Guardian' in col_name or 'Phone' in col_name:
			guardian_col_name.append(col_name)
			guardian_data.append(df[col_name])
	guardian_dict = dict(zip(guardian_col_name, guardian_data))
	return guardian_dict
'''


def main(filename1 = 'tutor.csv', filename2 = 'student.csv'):
	all_tutors = Tutor_Manager(filename1)
	all_students = Student_Manager(filename2)
	
	#open Tutors csv and turn each row into a Tutor instance
	with open(filename1, 'rb') as f1:
		result = chardet.detect(f.read())
	tutor_dict = pd.read_csv(filename1, encoding=result['encoding'])
	for row in tutor_dict.itertuples():	
		tut = Tutor(row)
		all_tutors.append(tut)

		
if __name__ == '__main__':
    main('tutor.csv', 'student.csv')

