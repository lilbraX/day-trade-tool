from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.models import User


def get_current_user(db: Session) -> User:
    user = db.execute(select(User).where(User.email == settings.default_user_email)).scalar_one_or_none()
    if user is None:
        user = User(email=settings.default_user_email, name="Demo User")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
