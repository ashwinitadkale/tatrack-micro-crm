from app import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key=True)
    inquiry_id = db.Column(db.Integer, db.ForeignKey("inquiries.id"), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="scheduled")
    deposit_amount = db.Column(db.Float, default=0.0)
    total_price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    inquiry = db.relationship("Inquiry", backref="sessions")

    def to_dict(self):
        return {
            "id": self.id,
            "inquiry_id": self.inquiry_id,
            "client_name": self.inquiry.client_name if self.inquiry else None,
            "tattoo_idea": self.inquiry.tattoo_idea if self.inquiry else None,
            "contact_info": self.inquiry.contact_info if self.inquiry else None,
            "session_date": self.session_date.isoformat() if self.session_date else None,
            "session_time": self.session_time,
            "status": self.status,
            "deposit_amount": self.deposit_amount or 0,
            "total_price": self.total_price or 0,
            "balance": max(0, (self.total_price or 0) - (self.deposit_amount or 0)),
        }
