from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from API.database import Base
from Models.associations_tables import association_sets


class Item(Base):
    __tablename__ = "Item"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    tags: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    collection_id: Mapped[int] = mapped_column(ForeignKey("Collection.id"))
    set_id: Mapped[Optional[List[int]]] = mapped_column(ForeignKey("Set.id"))
    color: Mapped[str] = mapped_column()

    sets: Mapped[List["Set"]] = relationship(  # noqa: F821f
        secondary=association_sets, back_populates="items"
    )
    collection: Mapped["Collection"] = relationship(  # noqa: F821
        back_populates="items"
    )
