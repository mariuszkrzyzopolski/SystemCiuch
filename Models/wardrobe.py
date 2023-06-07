from sqlalchemy.orm import Mapped, mapped_column, relationship

from API.database import Base


class Wardrobe(Base):
    __tablename__ = "Wardrobe"

    id: Mapped[int] = mapped_column(primary_key=True)
    mail: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    user: Mapped["User"] = relationship(back_populates="wardrobe")  # noqa: F821f
