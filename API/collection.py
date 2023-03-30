from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.requests import Request

from API.database import DB, get_database
from Models.collection import Collection
from Models.item import Item
from Models.set import Set

conn = get_database()
database = DB(conn)
router = APIRouter(prefix="/collection")


# TODO Patch for sets and items
@router.post("/set")
def post_set(top_id: int, pants_id: int, shoes_id: int):
    with Session(database.conn) as session:
        top = session.query(Item).get(top_id)
        pants = session.query(Item).get(pants_id)
        shoes = session.query(Item).get(shoes_id)
        new_set = Set(top=top, pants=pants, shoes=shoes)
        session.add(new_set)
        top.set_id = new_set.id
        pants.set_id = new_set.id
        shoes.set_id = new_set.id
        session.commit()
        session.refresh(new_set)
        return new_set


@router.get("/sets/{set_id}")
def get_set(set_id):
    with Session(database.conn) as session:
        q = select(Set).filter(Set.id == set_id)
        data = session.execute(q).mappings().first()
        return data


@router.get("/sets")
def get_sets():
    with Session(database.conn) as session:
        q = select(Set)
        data = session.execute(q).mappings().all()
        return data


@router.get("/")
def get_collection(request: Request):
    with Session(database.conn) as session:
        q = select(Collection).filter(Collection.id == request.session["collection"])
        data = session.execute(q).mappings().first()
        return data
