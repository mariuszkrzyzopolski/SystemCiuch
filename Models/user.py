from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from API.database import Base

class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key=True)
    mail: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    id_wardrobe: Mapped[Optional[int]] = mapped_column(ForeignKey("Wardrobe.id"))
    # wardrobe: Mapped["Wardrobe"] = relationship(back_populates="wardrobe")
    city:Mapped[str] = mapped_column()

# class User(BaseModel):
#     id: int
#     mail: str
#     city: str
#     id_warderobe: int
