"""
FastAPI with Pydantic models, path/query params, and a request body.
Uses a small in-memory list (no database yet) so you can focus on the API shape.

Run:
    cd day3/fastapi/code
    uvicorn models:app --reload --port 8000
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Pixel Quest API - models")

# ---- in-memory sample data ----
PLAYERS = [
    {"player_id": 1, "username": "hero_07", "country": "PK", "score": 4200},
    {"player_id": 2, "username": "mage_lily", "country": "US", "score": 5100},
    {"player_id": 3, "username": "elf_mona", "country": "PK", "score": 7300},
]


# ---- Pydantic models describe the shape of data in and out ----
class Player(BaseModel):
    player_id: int
    username: str
    country: str
    score: int = 0


class NewPlayer(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    country: str = Field(min_length=2, max_length=2)
    score: int = Field(default=0, ge=0)        # ge = greater-or-equal 0


@app.get("/players", response_model=list[Player])
def list_players(country: str | None = None):
    # query param ?country=PK filters the list
    if country:
        return [p for p in PLAYERS if p["country"] == country]
    return PLAYERS


@app.get("/players/{player_id}", response_model=Player)
def get_player(player_id: int):
    for p in PLAYERS:
        if p["player_id"] == player_id:
            return p
    # a clean 404 with a helpful message
    raise HTTPException(status_code=404, detail=f"player {player_id} not found")


@app.post("/players", response_model=Player, status_code=201)
def create_player(new: NewPlayer):
    player = {"player_id": len(PLAYERS) + 1, **new.model_dump()}
    PLAYERS.append(player)
    return player
