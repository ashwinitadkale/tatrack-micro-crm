from app import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    deposit_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    payment_status = db.Column(db.String(30), default="deposit_pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    session = db.relationship("Session", backref="payments")

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "client_name": self.session.inquiry.client_name if self.session and self.session.inquiry else None,
            "tattoo_idea": self.session.inquiry.tattoo_idea if self.session and self.session.inquiry else None,
            "deposit_amount": self.deposit_amount or 0,
            "total_amount": self.total_amount or 0,
            "balance": max(0, (self.total_amount or 0) - (self.deposit_amount or 0)),
            "payment_status": self.payment_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
