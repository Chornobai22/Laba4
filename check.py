
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:chornobai2002@localhost:3306/bd')
connection = engine.connect()

session = sessionmaker(bind=engine)
s = session()



s.commit()
