from app import db
from datetime import datetime, date

class Reminder(db.Model):
    __tablename__ = "reminders"
    id = db.Column(db.Integer, primary_key=True)
    inquiry_id = db.Column(db.Integer, db.ForeignKey("inquiries.id"), nullable=False)
    reminder_date = db.Column(db.Date, nullable=False)
    note = db.Column(db.String(300))
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    inquiry = db.relationship("Inquiry", backref="reminders")

    def to_dict(self):
        today = date.today()
        return {
            "id": self.id,
            "inquiry_id": self.inquiry_id,
            "client_name": self.inquiry.client_name if self.inquiry else None,
            "tattoo_idea": self.inquiry.tattoo_idea if self.inquiry else None,
            "reminder_date": self.reminder_date.isoformat() if self.reminder_date else None,
            "note": self.note or "",
            "is_completed": self.is_completed,
            "is_overdue": (not self.is_completed and self.reminder_date < today) if self.reminder_date else False,
            "is_today": (self.reminder_date == today) if self.reminder_date else False,
        }
