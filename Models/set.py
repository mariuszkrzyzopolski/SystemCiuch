from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from API.database import Base

class Set(Base):
    __tablename__ = 'Set'

    id: Mapped[int] = mapped_column(primary_key=True)
    top: Mapped[int] = mapped_column()#ForeignKey("Item.id"))
    pants: Mapped[int] = mapped_column()#ForeignKey("Item.id"))
    shoes: Mapped[int] = mapped_column()#ForeignKey("Item.id"))
    # def __init__(self, top, pants, shoes):
    #     self.brand = top
    #     self.model = pants
    #     self.color = shoes
