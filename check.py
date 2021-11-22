import os
import random
from datetime import datetime
#from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

engine = create_engine('mysql://root:chornobai2002@localhost:3306/bd')
connection = engine.connect()

Session = sessionmaker(bind = engine)
session = Session()

#for n in range(1, 2):
#    fv = User(id = n,name = 'Dima', surname = 'Chornobai',
#        username = 'Chornobai22', password = '1234', accessusers= 'all')
#print(f"Adding FV0{n}.")
#session.add(fv)

session.commit()
