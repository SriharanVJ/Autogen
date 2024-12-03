from sqlalchemy import Column, create_engine,ForeignKey,String,Integer,CHAR,select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_url="postgresql+psycopg2://postgres:........@localhost:5432/TestCase1"


engine=create_engine(db_url)
con=engine.connect()

base=declarative_base()

class Hospital(base):
    __tablename__="Patient"
    
    id = Column("id",Integer , primary_key=True)
    name = Column("Name",String)
    age=Column("Age",Integer)
    email=Column("Email",String)
    ph_no=Column("Phone_Number",Integer)    
    
    
    def __init__(self,id,name,age,email,ph_no):
        self.id
        self.name
        self.age
        self.email
        self.ph_no
        
    def __repr__(self):
        return f"({self.id}),{self.name},({self.age}),{self.email},({self.ph_no})"
    
base.metadata.create_all(bind=engine)

Session=sessionmaker(bind=engine)
session=Session()

Hospital=Hospital(10,"raju",54,"rajuraju@gmail.com",3695847152)
session.add(Hospital)
session.commit()
result=session.scalars(select(Hospital)).all()

print(result)
