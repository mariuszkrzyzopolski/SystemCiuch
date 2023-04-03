from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from API.database import Base


class Set(Base):
    __tablename__ = "Set"

    id: Mapped[int] = mapped_column(primary_key=True)
    top: Mapped[int] = ForeignKey("Item.id")
    pants: Mapped[int] = ForeignKey("Item.id")
    shoes: Mapped[int] = ForeignKey("Item.id")
