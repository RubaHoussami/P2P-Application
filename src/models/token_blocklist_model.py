from extensions import db

class TokenBlocklist(db.Model):
    __tablename__ = 'token blocklist'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    date = db.Column(db.DateTime, nullable=False)
