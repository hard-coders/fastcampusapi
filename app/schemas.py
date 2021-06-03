from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    score: int

    class Config:
        orm_mode = True
