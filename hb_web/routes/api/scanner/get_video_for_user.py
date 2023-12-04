from flask import g, request, current_app, abort
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from database import engine
from models.user import *


def video_urls(users_gender, user_seeking):
    # URLs from server
    stand = "/static/videos/Standard.mp4"
    trad = "/static/videos/Trad.mp4"
    gayF = "/static/videos/Female.mp4"
    gayM = "/static/videos/Male.mp4"

    seeks = [False, False, False]  # Ensure correct order of URLs returned
    urls = [stand]  # We always have standard video returned

    # Handle error if referencing user that has not filled out survey
    if user_seeking == 'NULL' or users_gender == 'NULL':
        abort(404, 'Referenced NULL in SQL')

    for n in user_seeking:
        # Split the object fields to get the specified genders
        seeking = str(n.seeking).split('.')[1]
        gender = str(users_gender).split('.')[1]
        current_app.logger.debug(f"SEEKING: {seeking}", f"GENDER: {gender}") # DEBUG
        # If OTHER, set gayF and gayM to true
        if seeking == 'OTHER':
            seeks[1] = True
            seeks[2] = True
        # If user seeking opposite gender, set traditional to true
        if seeking != gender and seeking != 'OTHER':
            seeks[0] = True
        # If user seeking same gender, set either gayF/gayM to true, depending on gender
        if seeking == gender:
            if gender == 'FEMALE':
                seeks[1] = True
            elif gender == 'MALE':
                seeks[2] = True

    current_app.logger.debug(seeks) # DEBUG

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
    
    urls = []

    with Session(engine) as session:
        stmt = select(User).where(User.id == request.authorization.token)
        result = session.execute(stmt)
        user = result.scalar_one_or_none()
        current_app.logger.debug(user) # DEBUG
        urls = video_urls(user.gender, user.seeking) # Get video URLS based on user preferences

    return {"videos": urls}


'''

'''