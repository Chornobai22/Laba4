
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:mysqlpass@127.0.0.1/ratings')
connection = engine.connect()

session = sessionmaker(bind=engine)
s = session()


#for n in range(1, 2):
#    fv = User(id = n,name = 'Dima', surname = 'Chornobai',
#        username = 'Chornobai22', password = '1234', accessusers= 'all')
#print(f"Adding FV0{n}.")
#session.add(fv)

s.commit()
