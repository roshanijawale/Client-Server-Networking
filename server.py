import os
import pickle
from connection import *

s.bind((host,port))

s.listen(1)

add,con = s.accept()

emps = []

menu = """
1. Insert Employee
2. Update Employee
3. Delete Employee
4. Search Employee
5. Display Employees
6. Exit
"""

#beginning of the program
def count_employees():
	if(len(emps)>0):
		return True
	else:
		return False
		
def print_menu():
	add.send(menu.encode())	
	op = int(add.recv(1024).decode())
	if(op==0):
		pass
	else:
		switcher(op)
	
def insert():
	res = add.recv(1024).decode()
	if(res == "insert"):
		e = add.recv(2048)
		e = pickle.loads(e)
		emps.append(e)
		add.send("record inserted".encode())
	else:
		add.send("Error ... Enter all details".encode())
	
def update():
	flag = "empty"
	
	if(count_employees()):
		flag = "rec_found"
		add.send(flag.encode())
		
		name = add.recv(1024).decode()
		
		flag = "fail"
		
		for i in range(0,len(emps)):
		
			if(emps[i].getName() == name):
				flag = "success"
				add.send(flag.encode())
				temp_emp = pickle.dumps(emps[i])
				add.send(temp_emp)
				res = add.recv(1024).decode()
				
				if(res == "update"):
					new_emp = add.recv(2048)
					new_emp = pickle.loads(new_emp)
					emps[i] = new_emp
					add.send("Updated Successfully".encode())
				else:
					add.send("Record is unchanged! try again ".encode())
					
				break
				
		if(flag == 'fail'):
			add.send(flag.encode())
	else:
		add.send(flag.encode())
		
def delete():
	flag = "empty"
	if(count_employees()):
		flag = "rec_found"
		add.send(flag.encode())
	
		name = add.recv(1024).decode()
		flag="fail"
		
		if(len(emps) == 0):
			flag = "empty"
			add.send(flag.encode())
		else:
			for i in range(0,len(emps)):
				if(emps[i].getName() == name):
					flag = "success"
					add.send(flag.encode())
					temp_emp = pickle.dumps(emps[i])
					add.send(temp_emp)	
					
					choice = add.recv(1024).decode()
					if(choice == "Y" or choice == "y"):
						emps.remove(emps[i])
						add.send("Deleted Successfully".encode())

					elif(choice == "N" or choice == "n"):
						add.send("Record is safe".encode())

					else:
						add.send("Something went wrong!".encode())
							
					break
			else:
				add.send(flag.encode())
	else:
		add.send(flag.encode())
		
def search():
	flag = "empty"
	if(count_employees()):
		flag = "rec_found"
		add.send(flag.encode())
		name = add.recv(1024).decode()
		
		flag = "fail"
		
		for i in range(0,len(emps)):
			if(emps[i].getName()==name):
				flag = "success"
				add.send(flag.encode())
				temp_emp = pickle.dumps(emps[i])
				add.send(temp_emp)		
				break
				
		if(flag == 'fail'):
			add.send(flag.encode())
	else:
		add.send(flag.encode())

def display():
	flag = "empty"
	if(count_employees()):
		flag = "rec_found"
		add.send(flag.encode())
	
		temp_emps = pickle.dumps(emps)
		add.send(temp_emps)
	else:
		add.send(flag.encode())
		
def exit():	
	add.send("Bye Bye".encode())	
	add.close()
	
def switcher(op):
	switch = {
		1 : insert,
		2 : update,
		3 : delete,
		4 : search,
		5 : display,
		6 : exit
	}
	func = switch.get(op)
	print(func())

while True:
	try:
		print_menu()
		os.system('cls') 
	except:
		print("client disconnect")
		break
