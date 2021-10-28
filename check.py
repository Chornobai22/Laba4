import os
import random
from datetime import datetime
#from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main  import user

engine = create_engine('mysql://ADMIN:Shapochka@127.0.0.1/bd1')
connection = engine.connect()

Session = sessionmaker(bind = engine)
session = Session()

################################################################################
# Uncomment the following block to create FV01 - FV09 in the Fv table.
################################################################################
for n in range(5, 6):
    fv = user(id = n,name = 'nune', surname = 'nune',
          username = 'nune', password = '1234', accessusers= 'all')
    print(f"Adding FV0{n}.")
    session.add(fv)

session.commit()
