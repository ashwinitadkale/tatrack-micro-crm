from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models.inquiry import Inquiry
from app.models.reminder import Reminder
from app.models.session import Session
from datetime import date

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard.html")

@dashboard_bp.route("/api/dashboard/stats")
@login_required
def stats():
    today = date.today()
    inquiries = Inquiry.query.filter_by(user_id=current_user.id).all()
    pending = [i for i in inquiries if i.status in ("new", "contacted", "consulted")]
    booked = [i for i in inquiries if i.status == "booked"]

    today_reminders = Reminder.query.join(Inquiry).filter(
        Inquiry.user_id == current_user.id,
        Reminder.reminder_date == today,
        Reminder.is_completed == False
    ).all()

    overdue_reminders = Reminder.query.join(Inquiry).filter(
        Inquiry.user_id == current_user.id,
        Reminder.reminder_date < today,
        Reminder.is_completed == False
    ).all()

    today_sessions = Session.query.join(Inquiry).filter(
        Inquiry.user_id == current_user.id,
        Session.session_date == today
    ).all()

    recent = sorted(inquiries, key=lambda x: x.created_at, reverse=True)[:6]

    return jsonify({
        "pending_inquiries": len(pending),
        "booked_sessions": len(booked),
        "today_reminders": len(today_reminders),
        "overdue_reminders": len(overdue_reminders),
        "today_sessions": len(today_sessions),
        "total_inquiries": len(inquiries),
        "recent_inquiries": [i.to_dict() for i in recent],
        "today_reminder_list": [r.to_dict() for r in today_reminders],
        "today_session_list": [s.to_dict() for s in today_sessions],
    })
