from sqlalchemy import Column, ForeignKey, Table

from API.database import Base

association_sets = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("Set.id")),
    Column("right_id", ForeignKey("Item.id")),
)
