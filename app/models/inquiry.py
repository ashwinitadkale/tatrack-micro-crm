from app import db
from datetime import datetime

class Inquiry(db.Model):
    __tablename__ = "inquiries"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    tattoo_idea = db.Column(db.Text)
    estimated_price = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default="new")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "contact_info": self.contact_info,
            "tattoo_idea": self.tattoo_idea or "",
            "estimated_price": self.estimated_price or 0,
            "status": self.status,
            "notes": self.notes or "",
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
