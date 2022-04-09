from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import Base, Post

engine = create_engine("mysql://root:my-secret-pw@127.0.0.1/mydb")

# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

class SqlEngine:
    session = None

    def __init__(self):
        pass

    def get_posts():
        session = Session()
        posts = session.query(Post).all()
        return posts