from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

Base = declarative_base()


class ImageDB(Base):
    __tablename__ = 'imagedb'

    id = Column(Integer, primary_key=True)
    image_file = Column(String)
    posx = Column(Integer)
    posy = Column(Integer)

    def __repr__(self):
        return "<ImageDB(image_file = '{}', pos = '{},{}'>".format(self.image, self.posx, self.posy)
