
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int

    model_config = ConfigDict(from_attributes=True)


class CartItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str

    model_config = ConfigDict(from_attributes=True)
