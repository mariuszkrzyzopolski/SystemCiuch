from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from API.database import Base


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    mail: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    id_collection: Mapped[int] = mapped_column(ForeignKey("Collection.id"))
    city: Mapped[str] = mapped_column()
    id_wardrobe: Mapped[Optional[int]] = mapped_column(ForeignKey("Wardrobe.id"))

    collection: Mapped["Collection"] = relationship(  # noqa: F821f
        back_populates="user"
    )
    wardrobe: Mapped["Wardrobe"] = relationship(back_populates="user")  # noqa: F821f
