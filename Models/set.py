from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from API.database import Base
from Models.associations_tables import association_sets


class Set(Base):
    __tablename__ = "Set"

    id: Mapped[int] = mapped_column(primary_key=True)
    items: Mapped[List["Item"]] = relationship(  # noqa: F821f
        secondary=association_sets, back_populates="sets"
    )
