from application.audio import BaseAudio
from application.databases import db, Column


class Podcast(BaseAudio):
    __tablename__ = "podcast"
    name = Column(db.String(100), nullable=False)
    host = Column(db.String(100), nullable=False)
    participents = Column(db.Text, nullable=False)
