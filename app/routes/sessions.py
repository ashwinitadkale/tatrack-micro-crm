from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models.session import Session
from app.models.inquiry import Inquiry
from datetime import datetime, date

sessions_bp = Blueprint("sessions", __name__)

@sessions_bp.route("/sessions")
@login_required
def sessions_page():
    return render_template("sessions.html")

@sessions_bp.route("/api/sessions", methods=["POST"])
@login_required
def create_session():
    data = request.json or {}
    if "inquiry_id" not in data or "session_date" not in data:
        return jsonify({"error": "inquiry_id and session_date required"}), 400
    inquiry = Inquiry.query.filter_by(id=data["inquiry_id"], user_id=current_user.id).first_or_404()
    inquiry.status = "booked"
    session = Session(
        inquiry_id=inquiry.id,
        session_date=datetime.strptime(data["session_date"], "%Y-%m-%d").date(),
        session_time=data.get("session_time", "TBD"),
        deposit_amount=data.get("deposit_amount", 0),
        total_price=data.get("total_price", inquiry.estimated_price or 0),
    )
    db.session.add(session)
    db.session.commit()
    return jsonify({"message": "Session booked", "session": session.to_dict()}), 201

@sessions_bp.route("/api/sessions", methods=["GET"])
@login_required
def get_sessions():
    sessions = Session.query.join(Inquiry).filter(
        Inquiry.user_id == current_user.id
    ).order_by(Session.session_date).all()
    return jsonify([s.to_dict() for s in sessions])

@sessions_bp.route("/api/sessions/today", methods=["GET"])
@login_required
def today_sessions():
    today = date.today()
    sessions = Session.query.join(Inquiry).filter(
        Inquiry.user_id == current_user.id,
        Session.session_date == today
    ).all()
    return jsonify([s.to_dict() for s in sessions])

@sessions_bp.route("/api/sessions/<int:id>", methods=["PUT"])
@login_required
def update_session(id):
    session = Session.query.join(Inquiry).filter(
        Session.id == id, Inquiry.user_id == current_user.id
    ).first_or_404()
    data = request.json or {}
    for field in ("status", "session_time", "deposit_amount", "total_price"):
        if field in data:
            setattr(session, field, data[field])
    if "session_date" in data:
        session.session_date = datetime.strptime(data["session_date"], "%Y-%m-%d").date()
    if session.status == "completed":
        session.inquiry.status = "completed"
    elif session.status == "cancelled":
        session.inquiry.status = "lost"
    db.session.commit()
    return jsonify({"message": "Session updated", "session": session.to_dict()})
