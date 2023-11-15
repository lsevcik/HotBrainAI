from flask import g, request, current_app
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from database import engine
from models.user import *


def handle_request():
    if not request.authorization and request.authorization.type != "bearer":
        return {}, 400
    
    with Session(engine) as session:
        stmt = select(User).where(User.id == request.authorization.token)
        result = session.execute(stmt)
        user = result.scalar_one_or_none()
        current_app.logger.debug(user.seeking)

    return {"videos": [""]}
