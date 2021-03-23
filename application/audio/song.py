from application.audio import BaseAudio
from application.databases import db, Column


class Song(BaseAudio):
    __tablename__ = "song"
    name = Column(db.String(100), nullable=False)
