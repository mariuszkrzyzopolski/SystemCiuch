from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from API.database import Base

class Item(Base):
    __tablename__ = 'Item'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    tags: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    collection_id: Mapped[int] = mapped_column(ForeignKey("Collection.id"))

    collection: Mapped["Collection"] = relationship(back_populates="items")
    # parents: Mapped[List["Set"]] = relationship()