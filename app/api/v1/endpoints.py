from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Pokemon
from app.schemas import PokemonCreate, Pokemon as PokemonSchema
import httpx
import yaml

router = APIRouter()

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

POKEAPI_URL = config["api"]["pokeapi_url"]

@router.get("/pokemons", response_model=list[PokemonSchema])
async def get_pokemons(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pokemon))
    pokemons = result.scalars().all()
    
    if not pokemons:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{POKEAPI_URL}?limit=100&offset=0")
            data = response.json()
            
            for pokemon in data["results"]:
                pokemon_details = await client.get(pokemon["url"])
                pokemon_data = pokemon_details.json()
                
                new_pokemon = Pokemon(
                    name=pokemon_data["name"],
                    image=pokemon_data["sprites"]["front_default"],
                    type=", ".join([t["type"]["name"] for t in pokemon_data["types"]])
                )
                db.add(new_pokemon)
            
            await db.commit()
            
            result = await db.execute(select(Pokemon))
            pokemons = result.scalars().all()
    
    return pokemons

@router.get("/pokemons/search")
async def search_pokemons(name: str = None, type: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Pokemon)
    
    if name:
        query = query.filter(Pokemon.name.ilike(f"%{name}%"))
    if type:
        query = query.filter(Pokemon.type.ilike(f"%{type}%"))
    
    result = await db.execute(query)
    pokemons = result.scalars().all()
    
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Pokemon found matching the criteria")
    
    return pokemons