from application.audio import BaseAudio
from application.databases import db, Column


class AudioBook(BaseAudio):
    __tablename__ = "audiobook"
    title = Column(db.String(100), nullable=False)
    author = Column(db.String(100), nullable=False)
    narrator = Column(db.String(100), nullable=False)
