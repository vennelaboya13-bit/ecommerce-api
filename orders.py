from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CartItem, Product, Order, User
from app.schemas import OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/{user_id}", response_model=OrderResponse, status_code=201)
def place_order(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    cart_items = db.query(CartItem).filter(
        CartItem.user_id == user_id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0.0

    for item in cart_items:
        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if product is None:
            raise HTTPException(
                status_code=400,
                detail=f"Product {item.product_id} not found"
            )

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        total_amount += product.price * item.quantity

    try:
        for item in cart_items:
            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            product.stock -= item.quantity

        order = Order(
            user_id=user_id,
            total_amount=round(total_amount, 2),
            status="Placed"
        )

        db.add(order)

        for item in cart_items:
            db.delete(item)

        db.commit()
        db.refresh(order)

        return order

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to place order"
        )


@router.get("/{user_id}", response_model=list[OrderResponse])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Order).filter(
        Order.user_id == user_id
    ).order_by(Order.id.desc()).all()
