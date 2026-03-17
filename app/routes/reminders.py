from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models.reminder import Reminder
from app.models.inquiry import Inquiry
from datetime import datetime, date

reminders_bp = Blueprint("reminders", __name__)

@reminders_bp.route("/reminders")
@login_required
def reminders_page():
    return render_template("reminders.html")

@reminders_bp.route("/api/reminders", methods=["POST"])
@login_required
def create_reminder():
    data = request.json or {}
    if "inquiry_id" not in data or "reminder_date" not in data:
        return jsonify({"error": "inquiry_id and reminder_date required"}), 400
    inquiry = Inquiry.query.filter_by(id=data["inquiry_id"], user_id=current_user.id).first_or_404()
    reminder = Reminder(
        inquiry_id=inquiry.id,
        reminder_date=datetime.strptime(data["reminder_date"], "%Y-%m-%d").date(),
        note=data.get("note", ""),
    )
    db.session.add(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder created", "reminder": reminder.to_dict()}), 201

@reminders_bp.route("/api/reminders", methods=["GET"])
@login_required
def get_reminders():
    reminders = Reminder.query.join(Inquiry).filter(
        Inquiry.user_id == current_user.id
    ).order_by(Reminder.is_completed, Reminder.reminder_date).all()
    return jsonify([r.to_dict() for r in reminders])

@reminders_bp.route("/api/reminders/today", methods=["GET"])
@login_required
def today_reminders():
    today = date.today()
    reminders = Reminder.query.join(Inquiry).filter(
        Inquiry.user_id == current_user.id,
        Reminder.reminder_date == today,
        Reminder.is_completed == False
    ).all()
    return jsonify([r.to_dict() for r in reminders])

@reminders_bp.route("/api/reminders/<int:id>/complete", methods=["PUT"])
@login_required
def complete_reminder(id):
    reminder = Reminder.query.join(Inquiry).filter(
        Reminder.id == id, Inquiry.user_id == current_user.id
    ).first_or_404()
    reminder.is_completed = True
    db.session.commit()
    return jsonify({"message": "Done", "reminder": reminder.to_dict()})

@reminders_bp.route("/api/reminders/<int:id>", methods=["DELETE"])
@login_required
def delete_reminder(id):
    reminder = Reminder.query.join(Inquiry).filter(
        Reminder.id == id, Inquiry.user_id == current_user.id
    ).first_or_404()
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({"message": "Deleted"})
