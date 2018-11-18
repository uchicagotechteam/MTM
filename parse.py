#Lauren Li
#
#MTM
#
#This file contains the implementation of Student, Tutor, Student_Manager, Tutor_Manager, and Guardian classes from specified csv files.

import chardet
import pandas as pd
import csv

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

	def __str__(self):
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
		self.tutor_matches = []

	def __repr__(self):
		return f'Student({self.first_name}, {self.last_name})'
	
	def __str__(self):
		return f'Student({self.first_name}, {self.last_name})'



class Student_Manager:

	def __init__(self, filename):
		self.students = []

		with open(filename, 'rb') as f:
			result = chardet.detect(f.read()) #identify encoding code needed for pandas read_csv
		student_dict = pd.read_csv(filename, encoding=result['encoding'])
		student_dict.fillna(0, inplace = True)
		all_col_names = list(student_dict) #list of dataframe column names

		def add_students(df):
			students = []
			for i, row in df.iterrows(): #row is a panda Series

				def guardian_info():
					guardian_dict = {} 
					for col_name in all_col_names: 
						if 'scholarship' in col_name or 'Guardian' in col_name or 'Phone' in col_name: #check for colnames with Guardian info 
							guardian_dict[col_name] = row.get(col_name)
					return guardian_dict

				#create Guardian of all student(s) in this row
				guardian_dict = guardian_info()
				student_guardian = Guardian(guardian_dict) #create Guardian of all students in this row

				#start parsing students
				for i in range(1, 5): #each row has max 4 students
					name = f'Student {i} First Name'
					student_i = df.columns.get_loc(name) #index of Student's first name
					another_student_col = 'Do you have another student applying to MTM?' #column between students
					if i==1: #Student one
						end_student_i = df.columns.get_loc(another_student_col) #Student one ends at first column that asks Do you have another student..?
					elif i==2: #Student two
						if row.get(another_student_col).upper() == 'YES' or row.get(name): #second student exists
							next_student_col = another_student_col + f'.{i-1}'
							end_student_i = df.columns.get_loc(next_student_col) #end of Student 2 ends with 'Do you have another student..?.1'
						else:
							break
					else: #Student three or four
						if row.get(another_student_col + f'.{i-2}').upper() == 'YES' or row.get(name):
							next_student_col = another_student_col + f'.{i-1}'
							end_student_i = df.columns.get_loc(next_student_col)
						else:
							break
					student_dict = {}
					for i in range(student_i, end_student_i):
						col_name = df.columns[i]
						val = row.get(col_name)
						student_dict[col_name] = val
					students.append(Student(student_dict, student_guardian))
					
			return students

		self.students = add_students(student_dict)

	def __repr__(self):
		return f'{self.students}'

	def __str__(self):
		return f'{self.students}'


class Tutor:
	def __init__(self, tutor_dict):
		'''
		Initialize every instance of Tutor with a dictionary with one tutor's informtion.
		'''
		self.name = tutor_dict['Full Name']
		self.subjects = [] #need to find way to incorporate written in subjects; other two columns: tutor_dict['What subjects are you comfortable helping your student with?'] + tutor_dict['If you answered yes to the previous question, which AP/IB tests are you comfortable tutoring?']
		self.grades = tutor_dict['What grade levels are you comfortable tutoring? (please check all that apply)'].split(',')

		if tutor_dict["Are you an international student? (We need this information to ensure you're paid directly by MTM, which keeps you from violating the terms of your visa.)"] == 'Yes':
			self.intl_student = 1
		else:
			self.intl_student = 0

		if tutor_dict['Are you comfortable working with students with disabilities including but not limited to autism, ADHD, and dyslexia? (Your honesty with this question helps us ensure that all students get a tutor who can fully address their needs.)'] == 'Yes, I am comfortable with this although I have no experience tutoring students with disabilities.':
			self.disabl = 1
		else:
			self.disabl = 0

		if tutor_dict['Would you prefer to do in-person or online (i.e. via Skype, webwhiteboard, and other programs) tutoring?'] == 'In-person':
			self.tutor_method = 1
		elif tutor_dict['Would you prefer to do in-person or online (i.e. via Skype, webwhiteboard, and other programs) tutoring?'] == 'Either is fine':
			self.tutor_method = 0
		else: #online only
			self.tutor_method = -1

		self.max_students = int(tutor_dict["How many students would you like to take on? (Keep in mind that most families want to meet twice a week for 1-1.5 hours.)"])
		self.num_students = 0
		self.matched_students = []

	def __repr__(self):
		return f'Tutor({self.name}), Matched students: {self.matched_students}'

	def __str__(self):
		return f'Tutor({self.name}), Matched students: {self.matched_students}'



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
				tut = Tutor(row)
				self.tutors.append(tut)

	def __repr__(self):
		return f'{self.tutors}'
	
	def __str__(self):
		return f'{self.tutors}'


def main(filename1 = 'tutor.csv', filename2 = 'student.csv'):
	all_tutors = Tutor_Manager(filename1)
	all_students = Student_Manager(filename2)


if __name__ == '__main__':
	main('tutor.csv', 'student.csv')



