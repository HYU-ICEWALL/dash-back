from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

from conf import db_host, db_id, db_pwd, db_name

engine = create_engine('mysql+mysqlconnector://%s:%s@%s/%s?charset=utf8' % (db_id, db_pwd, db_host, db_name), echo=True)

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	from models import User
	
	d = User('neo91', '102030')
	
	from database import db_session
	db_session = scoped_session(db_session)
	db_session.add(d)


	db_session.commit()
	db_session.remove()
