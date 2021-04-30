import pickle
import os
import time
from connection import *
from emp import Emp

s.connect((host,port))

#beginning of the program

def get_menu():
	menu = s.recv(1024).decode()
	print(menu)
	op = input("enter option : ")
	
	switcher(op)

def insert():
	e = Emp()
	e.set(input("Name : "),input ("Age : "),input("Sal : "))
	if(e.valid()):
		#if valid record is there
		s.send("insert".encode())
		e = pickle.dumps(e)
		s.send(e)
		res = s.recv(1024).decode()
		return res
	else:
		#if invalid record is there
		s.send("error".encode())
		return s.recv(1024).decode()

def update():
	#check if no records in list
	if(s.recv(1024).decode() != "empty"):
		name = input("Enter Name of Employee: ")
		s.send(name.encode())
		
		res=s.recv(1024).decode()
		
		if(res == "success"):
			e = s.recv(1024)
			e = pickle.loads(e)
			
			print("Name\t\tAge\tSalary")	
			e.disp()
			
			temp_emp = Emp()
			
			temp_emp.name = input("Enter Name : ")
			temp_emp.age = input("Enter Age : ")
			temp_emp.sal = input("Enter Salary : ")
			
			if(temp_emp.valid()):
				s.send("update".encode())
				temp_emp = pickle.dumps(temp_emp)
				s.send(temp_emp)
				res = s.recv(1024).decode()
				return res
				
			else:
				s.send("keep safe".encode())
				return s.recv(1024).decode()
			
		else:
			return "Record Not Found"
	else:
		return "No records Found"

def delete():
	#check if no records in list
	if(s.recv(1024).decode() != "empty"):
		name = input("Enter Name : ")
		s.send(name.encode())
		
		res = s.recv(1024).decode()
		
		if(res == "empty"):
			return "data is empty so insert records"
			
		elif(res == "success"):
			temp_emp = Emp()
			temp_emp = s.recv(2048)
			temp_emp = pickle.loads(temp_emp)
			print("Name\t\tAge\tSalary")	
			temp_emp.disp()
			
			choice = input("Do You want to delete this Record? Y/N : ")

			s.send(choice.encode())
			return s.recv(1024).decode()
		else:
			return "Record not found"
	else:
		return "No records Found"

def search():
#check if no records in list
	if(s.recv(1024).decode() != "empty"):
		name = input("Enter Name of Employee: ")
		s.send(name.encode())
		
		res=s.recv(1024).decode()
		
		if(res == "success"):
			e = s.recv(1024)
			e = pickle.loads(e)
			
			print("Name\t\tAge\tSalary")	
			e.disp()
			
			return "Record Found"
		else:
			return "Ops Record Not Found"
	else:
		return "No records Found"
	
def display():
#check if no records in list
	if(s.recv(1024).decode() != "empty"):
		emps = s.recv(2048)
		emps = pickle.loads(emps)
		print("Name\t\tAge\tSalary")	
		for e in emps:
			e.disp()
		return "Total {} Records".format(len(emps))
	else:
		return "No records Found"

def exit():	
	try:
		res=s.recv(1024).decode()
		s.close()
		return res
	except:
		return "disconnect successfully"
		
		
def switcher(op):
	switch = {
		1 : insert,
		2 : update,
		3 : delete,
		4 : search,
		5 : display,
		6 : exit
	}
	try:
		func = switch.get(int(op),"Invalid Choice" )
		if func!='Invalid Choice':
			s.send(op.encode())
			print(func())
		elif(func == "Invalid Choice"):
			s.send('0'.encode())
			print("Invalid Choice")
	except:
		s.send('0'.encode())
		print("Invalid Choice")
'''		
while True:
	get_menu()
'''	
while True:
	try:
		get_menu()
		time.sleep(2)
		os.system('cls')
	except OSError:
		break