from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.token import Token
from app.utils.security import verify_password, create_access_token, create_refresh_token
from app.services.user import get_user_by_email


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    Returns the user if authentication succeeds, None otherwise.
    """
    user = get_user_by_email(db, email)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def create_tokens(user: User) -> Token:
    """Create access and refresh tokens for a user."""
    token_data = {"sub": user.email, "user_id": user.id}
    
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
