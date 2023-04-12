from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from API.database import Base
from Models.item import Item


class Collection(Base):
    __tablename__ = "Collection"

    id: Mapped[int] = mapped_column(primary_key=True)
    items: Mapped[List[Item]] = relationship(back_populates="collection")
    user: Mapped["User"] = relationship(back_populates="collection")  # noqa: F821f
