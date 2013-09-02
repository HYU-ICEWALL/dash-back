from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
import datetime
from sqlalchemy.sql import select
from database import Base

class User(Base):
	__tablename__ = 'users'
	idx = Column(Integer, autoincrement=True, primary_key=True, unique=True)
	username = Column(String(20), unique=True)
	password = Column(String(64), unique=False)
	fid = Column(String(30), unique=False)
	major = Column(String(20), unique=False)
	
	def __init__(self, username='', password='', fid='', major=''):
		self.username = username
		self.password = password
		self.fid = fid
		self.major = major
		
		
	def __repr__(self):
		return "User (%s, %s, %s, %s)" % (self.username, self.password, self.fid, self.major)


	def checkDup(self, uname):
		usr = self.query.filter(User.username==uname).first()
		if usr == None:
			return False
		
		return True

	def checkLogin(self, uname, pwd):
		usr = self.query.filter(User.username==uname, User.password==pwd).first()

		if usr == None:
			return False

		return True
