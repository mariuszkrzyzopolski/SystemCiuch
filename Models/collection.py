from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from API.database import Base
from Models.item import Item


class Collection(Base):
    __tablename__ = "Collection"

    id: Mapped[int] = mapped_column(primary_key=True)
    items: Mapped[List[Item]] = relationship(back_populates="collection")
    id_wardrobe: Mapped[int] = mapped_column(ForeignKey("Wardrobe.id"))
    id_user: Mapped[int] = mapped_column(ForeignKey("User.id"))

    # user: Mapped["User"] = relationship(back_populates="collection")
    # wardrobe: Mapped["Wardrobe"] = relationship(back_populates="collection")
