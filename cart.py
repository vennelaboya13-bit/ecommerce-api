from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CartItem, Product
from app.schemas import CartItemCreate, CartItemResponse

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])


@router.post("/{user_id}", response_model=CartItemResponse, status_code=201)
def add_to_cart(
        user_id: int,
        item_data: CartItemCreate,
        db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == item_data.product_id
    ).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < item_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == item_data.product_id
    ).first()

    if existing_item:
        new_quantity = existing_item.quantity + item_data.quantity

        if product.stock < new_quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock for requested quantity"
            )

        existing_item.quantity = new_quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    cart_item = CartItem(
        user_id=user_id,
        product_id=item_data.product_id,
        quantity=item_data.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


@router.get("/{user_id}", response_model=list[CartItemResponse])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(CartItem).filter(
        CartItem.user_id == user_id
    ).all()


@router.delete("/{user_id}/{item_id}")
def remove_from_cart(
        user_id: int,
        item_id: int,
        db: Session = Depends(get_db)
):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    ).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item removed from cart successfully"}
