from datetime import datetime, timezone
from typing import List
from sqlalchemy import (
  ForeignKey,
  func
)
from sqlalchemy.orm import (
  DeclarativeBase, 
  Mapped, mapped_column,
  relationship
)


class TableModel(DeclarativeBase):
  pass



class ProductCategoryTable(TableModel):
  __tablename__ = "product_category"
  
  id:         Mapped[int]      = mapped_column(primary_key=True)
  name:       Mapped[str]      = mapped_column(unique=True)
  created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
  
  products: Mapped[List["ProductTable"]] = relationship(back_populates="product_category")
                                     

class ProductTable(TableModel):
  __tablename__ = "product"
  
  id:         Mapped[int]      = mapped_column(primary_key=True)
  name:       Mapped[str]      = mapped_column(unique=True)
  created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
  
  product_category_id: Mapped[int]               = mapped_column(ForeignKey("product_category.id"))
  product_category:    Mapped["ProductCategoryTable"] = relationship(back_populates="products") 
  
