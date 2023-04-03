from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from API.database import Base
from Models.associations_tables import association_sets


class Set(Base):
    __tablename__ = "Set"

    id: Mapped[int] = mapped_column(primary_key=True)
    # top: Mapped[int] = ForeignKey("Item.id")
    # pants: Mapped[int] = ForeignKey("Item.id")
    # shoes: Mapped[int] = ForeignKey("Item.id")
    items: Mapped[List["Item"]] = relationship(secondary=association_sets,back_populates="sets")
