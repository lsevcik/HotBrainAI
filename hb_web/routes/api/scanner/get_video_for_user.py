from flask import g, request, current_app, abort
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from database import engine
from models.user import *


def video_urls(users_gender, user_seeking):
    # URLs that need to be changed to return correct ones from server. Not sure how to get the correct ones
    stand = 'STANDARD URL'
    trad = 'TRAD URL'
    gayF = 'FEMALE URL'
    gayM = 'MALE URL'

    seeks = [False, False, False]  # Ensure correct order of URLs returned
    urls = [stand]  # We always have standard video returned

    # Handle error if referencing user that has not filled out survey
    if user_seeking == 'NULL' or users_gender == 'NULL':
        abort(404, 'Referenced NULL in SQL')

    for n in user_seeking:
        # If OTHER, set gayF and gayM to true
        if n == 'OTHER':
            seeks[1] = True
            seeks[2] = True
        # If user seeking opposite gender, set traditional to true
        if n != users_gender and n != 'OTHER':
            seeks[0] = True
        # If user seeking same gender, set either gayF/gayM to true, depending on gender
        if n == users_gender:
            if users_gender == 'FEMALE':
                seeks[1] = True
            elif users_gender == 'MALE':
                seeks[2] = True

    # Append URLs depending on if they have been selected. Gives correct order.
    if seeks[0]:
        urls.append(trad)
    if seeks[1]:
        urls.append(gayF)
    if seeks[2]:
        urls.append(gayM)
    return urls


def handle_request():
    if not request.authorization and request.authorization.type != "bearer":
        return {}, 400

    with Session(engine) as session:
        stmt = select(User).where(User.id == request.authorization.token)
        result = session.execute(stmt)
        user = result.scalar_one_or_none()
        current_app.logger.debug(user.seeking)

    return {"videos": [""]}


'''

'''