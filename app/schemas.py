from pydantic import BaseModel

class PokemonBase(BaseModel):
    name: str
    image: str
    type: str

class PokemonCreate(PokemonBase):
    pass

class Pokemon(PokemonBase):
    id: int

    class Config:
        orm_mode = True