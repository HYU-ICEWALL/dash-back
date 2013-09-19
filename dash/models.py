from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
import datetime
from sqlalchemy.sql import select
from database import Base
import hashlib

class User(Base):
	__tablename__ = 'users'
	idx = Column(Integer, autoincrement=True, primary_key=True, unique=True)
	username = Column(String(20), unique=True)
	password = Column(String(64), unique=False)
	fid = Column(String(30), unique=False)
	major = Column(String(20), unique=False)
	
	def __init__(self, username='', password='', fid='', major=''):
		self.username = username
		self.password = hashlib.sha256(password).hexdigest()
		self.fid = fid
		self.major = major
	
	def getUser(self):
		dic = {}
		dic['id'] = self.idx
		dic['email'] = self.username
		dic['fb_id'] = self.fid
		dic['major'] = self.major

		return dic
			
	def __repr__(self):
		return "User (%s, %s, %s, %s)" % (self.username, self.password, self.fid, self.major)


	def checkDup(self):
		usr = self.query.filter(User.username==self.username).first()
		if usr == None:
			return False
		
		return True

	def checkLogin(self):
		usr = self.query.filter(User.username==self.username, User.password==self.password).first()
		if usr == None:
			return False
		self.username = usr.username
		self.fid = usr.fid
		self.major = usr.major
		self.idx = usr.idx
		self.password = '00000000'

		return True
	def is_authenticated(self) :
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.idx)

	
