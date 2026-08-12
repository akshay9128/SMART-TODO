from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse
from app.core.security import hash_password,verify_password,create_access_token
from app.core.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",response_model=UserResponse)
def create_user(
    user_data:UserCreate,
    db:Session=Depends(get_db)
):
    existing_user=(
        db.query(User)
        .filter(
            (User.username==user_data.username) |
            (User.email==user_data.email)
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username And Email Already Exists"
        )

    user=User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login")
def login(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.username == form_data.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me",response_model=UserResponse)
def get_me(
    current_user:User=Depends(get_current_user)
):
    return current_user