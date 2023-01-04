from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

many_to_many = Table(
    'many_to_many',
    Base.metadata,
    Column('tags_id', Integer, ForeignKey('tags.id')),
    Column('quotes_id', Integer, ForeignKey('quotes.id')),
)


class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    author_name = Column(String(60), nullable=False)
    born_date = Column(String(60), nullable=True)
    born_location = Column(String(60), nullable=True)
    author_url = Column(String(100), nullable=True)


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(60))


class Quotes(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    quote = Column(String(300), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'))
    tags = relationship('Tags', secondary=many_to_many, backref='tags')


engine = create_engine('sqlite:///quotes.db.sqlite3', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)