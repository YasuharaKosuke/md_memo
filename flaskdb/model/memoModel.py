from flaskdb import db
from sqlalchemy.dialects.postgresql import TIMESTAMP as Timestamp

class Memo(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_name = db.Column(db.String(64), nullable=False)
    share = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(Timestamp, nullable=False)

    def __repr__(self):
        return "<Memo %r>" % self.id
