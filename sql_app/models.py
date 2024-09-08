from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
  DeclarativeBase, 
  Mapped, mapped_column,
  relationship
)


class ORM_Base(DeclarativeBase):
  pass



class ORM_ProductCategory(ORM_Base):
  __tablename__ = "product_category"
  
  id:         Mapped[int]      = mapped_column(primary_key=True)
  name:       Mapped[str]      = mapped_column(unique=True)
  created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
  
  products: Mapped[List["ORM_Product"]] = relationship(back_populates="product_category")
                                     

class ORM_Product(ORM_Base):
  __tablename__ = "product"
  
  id:         Mapped[int]      = mapped_column(primary_key=True)
  name:       Mapped[str]      = mapped_column(unique=True)
  created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
  
  product_category_id: Mapped[Optional[int]]         = mapped_column(ForeignKey("product_category.id"))
  product_category:    Mapped["ORM_ProductCategory"] = relationship(back_populates="products") 
  
