from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    backdrop_path: str | None = None
    poster_path: str | None = None
    vote_average: float = 0 