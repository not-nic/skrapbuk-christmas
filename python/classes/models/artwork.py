from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from python.classes.database import database
from sqlalchemy.sql import func

class Artwork(database.Model):
    id = Column(Integer, primary_key=True)
    created_by = Column(String(255), ForeignKey('user.snowflake'))
    image_path = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())

    def __init__(self, created_by, image_path, created_at):
        self.created_by = created_by,
        self.image_path = image_path,
        self.created_at = created_at
