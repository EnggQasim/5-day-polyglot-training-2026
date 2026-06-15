# FastAPI — Step 2: Pydantic models and endpoints

Now we describe our data with **Pydantic models** and add real endpoints: path parameters, query parameters, a request body, and proper errors. We use a small in-memory list first (no database yet) so we can focus on the API shape. File: [`code/models.py`](code/models.py).

Run it:
```bash
cd day3/fastapi/code
uvicorn models:app --reload --port 8000
```

---

## Pydantic models = the shape of your data

A **Pydantic model** is a Python class that describes what a piece of data looks like. FastAPI uses it to **validate** input and to **document** output.

```python
from pydantic import BaseModel, Field

class Player(BaseModel):
    player_id: int
    username: str
    country: str
    score: int = 0

class NewPlayer(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    country: str = Field(min_length=2, max_length=2)
    score: int = Field(default=0, ge=0)     # ge = must be >= 0
```

If someone POSTs a `username` of 1 character, or a `score` of -5, FastAPI **rejects it automatically** with a clear error — you write no validation code.

---

## Path parameters

A value baked into the URL, like the id in `/players/2`:

```python
@app.get("/players/{player_id}", response_model=Player)
def get_player(player_id: int):
    for p in PLAYERS:
        if p["player_id"] == player_id:
            return p
    raise HTTPException(status_code=404, detail=f"player {player_id} not found")
```

- `{player_id}` in the path becomes the `player_id` argument. Declaring it `int` means FastAPI converts and validates it (a non-number returns a clean 422 error).
- `HTTPException(status_code=404, ...)` returns a proper **404 Not Found** with a message. Returning the right status codes is part of a good API.

## Query parameters

Optional values after `?`, like `/players?country=PK`:

```python
@app.get("/players", response_model=list[Player])
def list_players(country: str | None = None):
    if country:
        return [p for p in PLAYERS if p["country"] == country]
    return PLAYERS
```

A function argument that is **not** in the path becomes a query parameter. `country: str | None = None` makes it optional.

## Request body (POST)

To **create** something, the client sends JSON in the body; FastAPI parses it into your model:

```python
@app.post("/players", response_model=Player, status_code=201)
def create_player(new: NewPlayer):
    player = {"player_id": len(PLAYERS) + 1, **new.model_dump()}
    PLAYERS.append(player)
    return player
```

- The `new: NewPlayer` argument tells FastAPI "read the JSON body and validate it against `NewPlayer`".
- `status_code=201` = the HTTP code for "Created".

---

## See it all in /docs

Open **http://localhost:8000/docs**. Every endpoint, every model, and every validation rule is documented automatically. Try:
- `GET /players` then `GET /players?country=PK`.
- `GET /players/2` (works) and `GET /players/999` (clean 404).
- `POST /players` with a 1-letter username — watch it get rejected with a helpful message.

➡️ Next: **[03-async-and-databases.md](03-async-and-databases.md)** — make it async and connect to real data.

---

## ⭐ Must-learn from this topic

- **Pydantic models** — describe & validate data with `BaseModel` + `Field`.
- **Path vs query params** — `/players/{id}` vs `/players?country=PK`.
- **Request body** — a model argument parses & validates JSON.
- **Status codes & errors** — `HTTPException`, `status_code=201`/`404`.

### 📚 Official docs
- [Path parameters](https://fastapi.tiangolo.com/tutorial/path-params/) and [Query parameters](https://fastapi.tiangolo.com/tutorial/query-params/).
- [Request body](https://fastapi.tiangolo.com/tutorial/body/) — POST with Pydantic.
- [Handling errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) — `HTTPException`.
- [Pydantic docs](https://docs.pydantic.dev/latest/) — models & validation.
