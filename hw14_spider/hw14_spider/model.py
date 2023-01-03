from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

many_to_many = Table(
    "many_to_many",
    Base.metadata,
    Column("tags_id", Integer, ForeignKey("tags.id")),
    Column("quotes_id", Integer, ForeignKey("quotes.id")),
)


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    author_name = Column(String(50), nullable=False)
    birthday_and_place_of_born = Column(String(50), nullable=True)
    author_url = Column(String(50), nullable=True)


class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String(50))


class Quotes(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    quote = Column(String(50))
    author_id = Column(Integer, ForeignKey('person.id', ondelete="CASCADE"))
    tags = relationship("Tags", secondary=many_to_many, backref="tags")


engine = create_engine('sqlite:///scrapy_data.db.sqlite3', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)