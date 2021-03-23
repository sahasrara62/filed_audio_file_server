from application.databases import db, Model, SurrogatePK, db, Column
from datetime import datetime


class BaseAudio(SurrogatePK, Model):
    __abstract__ = True
    uploaded_time = Column(
        db.DateTime, default=db.func.now(), nullable=False, onupdate=datetime.utcnow()
    )
    duration_time = Column(db.Integer, default=0, nullable=False)


from .song import Song
from .audiobook import AudioBook
from .podcast import Podcast


audiofiletype = {"song": Song, "audiobook": AudioBook, "podcast": Podcast}
