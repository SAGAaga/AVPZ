from sqlalchemy import (
    Column,
    Integer,
    String,
)
import bcrypt

from .meta import Base


class SuperUser(Base):
    __tablename__ = "superuser"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def validate_password(self, password):
        expected_hash = password.encode("utf8")
        return bcrypt.checkpw(expected_hash, self.password.encode("utf8"))

    def hash_password(self, password):
        pwhash = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        return pwhash.decode("utf8")
