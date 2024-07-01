from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Pokemon
from app.schemas import PokemonCreate, Pokemon as PokemonSchema
import httpx
import yaml
from typing import List
from typing import Optional


router = APIRouter()

with open("config.yaml", "r") as f:
    config: dict = yaml.safe_load(f)

POKEAPI_URL: str = config["api"]["pokeapi_url"]
MAX_POKEMON: int = 100  # Maximum number of Pokemon to fetch and store

@router.get("/pokemons", response_model=List[PokemonSchema])
async def get_pokemons(
    limit: int = Query(default=20, ge=1, le=MAX_POKEMON),
    db: AsyncSession = Depends(get_db)
) -> List[PokemonSchema]:
    # Check how many Pokemon are in the database
    result = await db.execute(select(func.count()).select_from(Pokemon))
    count: int = result.scalar()
    
    # If we don't have all Pokemon in the database, fetch them
    if count < MAX_POKEMON:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{POKEAPI_URL}?limit={MAX_POKEMON}")
            data: dict = response.json()
            
            for pokemon in data["results"]:
                # Check if this Pokemon already exists in the database
                existing_pokemon = await db.execute(select(Pokemon).filter(Pokemon.name == pokemon["name"]))
                if existing_pokemon.scalar_one_or_none() is None:
                    pokemon_details = await client.get(pokemon["url"])
                    pokemon_data: dict = pokemon_details.json()
                    
                    new_pokemon = Pokemon(
                        name=pokemon_data["name"],
                        image=pokemon_data["sprites"]["front_default"],
                        type=", ".join([t["type"]["name"] for t in pokemon_data["types"]])
                    )
                    db.add(new_pokemon)
            
            await db.commit()
    
    # Fetch the requested number of Pokemon from the database
    result = await db.execute(select(Pokemon).limit(limit))
    pokemons: List[Pokemon] = result.scalars().all()
    
    return pokemons

@router.get("/pokemons/search", response_model=List[PokemonSchema])
async def search_pokemons(
    name: Optional[str] = None,
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> List[PokemonSchema]:
    query = select(Pokemon)
    
    if name:
        query = query.filter(Pokemon.name.ilike(f"%{name}%"))
    if type:
        query = query.filter(Pokemon.type.ilike(f"%{type}%"))
    
    result = await db.execute(query)
    pokemons: List[Pokemon] = result.scalars().all()
    
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Pokemon found matching the criteria")
    
    return pokemons