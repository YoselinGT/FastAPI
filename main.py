from typing import Optional, List,Annotated

from fastapi import FastAPI, Path, Query,HTTPException,Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field

from fastapi.responses import JSONResponse
import secrets

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2023,
                "rating": 9.8,
                "category": "Acción"
            }
        }
    }


app = FastAPI()

security = HTTPBasic()

app.title = "BI de consumos de sign all"
app.version = "2.0.5.6"

movies:Movie = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Terror"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    }
];


@app.get('/login/basic', response_class=JSONResponse, tags=['auth'], status_code=200)
def get_login_basic(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get('/movies', response_class=JSONResponse, tags=['movies'], status_code=200)
def get_movies() -> List[Movie]:
    return movies


@app.get('/movies/{id}', response_class=JSONResponse, tags=['movies'], response_model=Movie, status_code=200)
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item, status_code=200)
    return JSONResponse(content=[], status_code=404)


@app.get('/movies/', response_class=JSONResponse, tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str =Query(min_length=5, max_length=15)) -> List[Movie]:
    return [item for item in movies if item['category'] == category]


@app.post('/movies/', response_class=JSONResponse, tags=['movies'], response_model=dict, status_code=2001)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return {"mensaje":"Se ha creado la pelicula"};


@app.put('/movies/{id}', response_class=JSONResponse, tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    movie.id = id
    for i, item in enumerate(movies):
        if item["id"] == id:
            movies[i] = movie;
    return {"mensaje":"Se ha actualizado la pelicula"};


@app.delete('/movies/{id}', response_class=JSONResponse, tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    print("movies",type(movies))
    for item in movies:
        print("item",item)
        print("type",type(item))
        print("id",item["id"])
        if item["id"] == id:
            movies.remove(item)
    return {"mensaje":"Se ha eliminado la pelicula"};
