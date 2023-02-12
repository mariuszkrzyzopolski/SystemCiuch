from pydantic import BaseModel

class User(BaseModel):
    id: int
    mail: str
    city: str
    id_warderobe: int