from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models.inquiry import Inquiry
from app.models.reminder import Reminder
from datetime import datetime, timedelta

inquiries_bp = Blueprint("inquiries", __name__)

@inquiries_bp.route("/inquiries")
@login_required
def inquiries_page():
    return render_template("inquiries.html")

@inquiries_bp.route("/api/inquiries", methods=["POST"])
@login_required
def create_inquiry():
    data = request.json or {}
    if not data.get("client_name") or not data.get("contact_info"):
        return jsonify({"error": "client_name and contact_info required"}), 400
    inquiry = Inquiry(
        user_id=current_user.id,
        client_name=data["client_name"],
        contact_info=data["contact_info"],
        tattoo_idea=data.get("tattoo_idea", ""),
        estimated_price=data.get("estimated_price", 0),
        notes=data.get("notes", ""),
        status=data.get("status", "new"),
    )
    db.session.add(inquiry)
    db.session.flush()
    follow_up = Reminder(
        inquiry_id=inquiry.id,
        reminder_date=(datetime.utcnow() + timedelta(days=2)).date(),
        note=f"Follow up with {inquiry.client_name}",
    )
    db.session.add(follow_up)
    db.session.commit()
    return jsonify({"message": "Inquiry created", "id": inquiry.id, "inquiry": inquiry.to_dict()}), 201

@inquiries_bp.route("/api/inquiries", methods=["GET"])
@login_required
def get_inquiries():
    inquiries = Inquiry.query.filter_by(user_id=current_user.id).order_by(Inquiry.created_at.desc()).all()
    return jsonify([i.to_dict() for i in inquiries])

@inquiries_bp.route("/api/inquiries/<int:id>", methods=["GET"])
@login_required
def get_inquiry(id):
    inquiry = Inquiry.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    data = inquiry.to_dict()
    data["reminders"] = [r.to_dict() for r in inquiry.reminders]
    data["sessions"] = [s.to_dict() for s in inquiry.sessions]
    return jsonify(data)

@inquiries_bp.route("/api/inquiries/<int:id>", methods=["PUT"])
@login_required
def update_inquiry(id):
    inquiry = Inquiry.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    data = request.json or {}
    for field in ("client_name", "contact_info", "tattoo_idea", "estimated_price", "notes", "status"):
        if field in data:
            setattr(inquiry, field, data[field])
    db.session.commit()
    return jsonify({"message": "Updated", "inquiry": inquiry.to_dict()})

@inquiries_bp.route("/api/inquiries/<int:id>", methods=["DELETE"])
@login_required
def delete_inquiry(id):
    inquiry = Inquiry.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(inquiry)
    db.session.commit()
    return jsonify({"message": "Deleted"})
