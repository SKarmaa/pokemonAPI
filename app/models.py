from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Pokemon(Base):
    __tablename__: str = "pokemons"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True)
    image: str = Column(String)
    type: str = Column(String)