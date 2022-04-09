from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    image = Column(String(255))
    author_id = Column(Integer)
    status = Column(String(255))
    type = Column(String(255))
    created_date = Column(Date)
    address = Column(String(255))
    contacts = Column(String(255))
    reward = Column(Integer)
    details = Column(String(255))
    breed = Column(String(255))
    gender = Column(String(255))
    age = Column(String(255))
    eye_color = Column(String(255))
    fur_color = Column(String(255))
    special_signs = Column(String(255))
    name = Column(String(255))
    nationality = Column(String(255))
    species = Column(String(255))

    def __repr__(self):
        return "<Post(id='%s')>" % (self.id)