from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
import datetime
from sqlalchemy.sql import select
from database import Base
import hashlib
import string
import random

class User(Base):
	__tablename__ = 'users'
	idx = Column(Integer, autoincrement=True, primary_key=True, unique=True)
	email = Column(String(20), unique=True)
	password = Column(String(64), unique=False)
	fid = Column(String(30), unique=False)
	major = Column(String(20), unique=False)
	
	def __init__(self, email='', password='', fid='', major='', idx=-1):
		self.email = email
		self.password = hashlib.sha256(password).hexdigest()
		self.fid = fid
		self.major = major
		self.idx = idx
	
	def getUser(self):
		dic = {}
		dic['id'] = self.idx
		dic['email'] = self.email
		dic['fb_id'] = self.fid
		dic['major'] = self.major

		return dic

	def checkDup(self):
		usr = self.query.filter(User.email==self.email).first()
		if usr == None:
			return False
		
		return True

	def checkLogin(self):
		usr = self.query.filter(User.email==self.email, User.password==self.password).first()
		if usr == None:
			return False
		self.email = usr.email
		self.fid = usr.fid
		self.major = usr.major
		self.idx = usr.idx
		self.password = '00000000'

		return True
	

	def resetPassword(self):
		chars = string.ascii_letters + string.digits
		newpwd = ''.join(random.choice(chars) for x in range(10))
		usr = self.query.filter(User.email == self.email).update({ 'password' : hashlib.sha256(newpwd).hexdigest() })

		if usr == 0:
			return {"status" : False}
		else:
			return {"status" : True, "password" : newpwd}

	def delUser(self):
		usr = self.query.filter(User.email == self.email).delete()
		
		if usr == 0:
			return False
		else :
			return True
			
	def modify(self, dic):
		if 'password' in dic:
			dic['password'] = hashlib.sha256(dic['password']).hexdigest()

		usr = self.query.filter(User.email == self.email).update(dic)

		if usr == 0:
			return False
		else:
			return True
	
