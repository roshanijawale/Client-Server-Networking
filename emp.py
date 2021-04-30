class Emp:
	def __init__(self):
		self.name = ''
		self.age = 0
		self.sal = 0
	
	def set(self,name,age,sal):
		self.name = name
		self.age = age
		self.sal = sal
	
	def disp(self):
		print(self.name,"\t\t",self.age,"\t",self.sal,"\t")
	
	def valid(self):
		if(self.name!="" and self.age!="" and self.sal!=""):
			return True
		else:
			return False
		
	def getName(self):
		return self.name