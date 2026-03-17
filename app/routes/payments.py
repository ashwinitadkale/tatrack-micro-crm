from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models.payment import Payment
from app.models.session import Session
from app.models.inquiry import Inquiry

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/payments")
@login_required
def payments_page():
    return render_template("payments.html")

@payments_bp.route("/api/payments", methods=["POST"])
@login_required
def create_payment():
    data = request.json or {}
    if "session_id" not in data:
        return jsonify({"error": "session_id required"}), 400
    session = Session.query.join(Inquiry).filter(
        Session.id == data["session_id"], Inquiry.user_id == current_user.id
    ).first_or_404()
    deposit = float(data.get("deposit_amount", 0))
    total = float(data.get("total_amount", session.total_price or 0))
    if deposit >= total and total > 0:
        status = "fully_paid"
    elif deposit > 0:
        status = "deposit_received"
    else:
        status = "deposit_pending"
    payment = Payment(session_id=session.id, deposit_amount=deposit, total_amount=total, payment_status=status)
    session.deposit_amount = deposit
    session.total_price = total
    db.session.add(payment)
    db.session.commit()
    return jsonify({"message": "Payment recorded", "payment": payment.to_dict()}), 201

@payments_bp.route("/api/payments", methods=["GET"])
@login_required
def get_payments():
    payments = Payment.query.join(Session).join(Inquiry).filter(
        Inquiry.user_id == current_user.id
    ).order_by(Payment.created_at.desc()).all()
    return jsonify([p.to_dict() for p in payments])

@payments_bp.route("/api/payments/pending", methods=["GET"])
@login_required
def pending_payments():
    payments = Payment.query.join(Session).join(Inquiry).filter(
        Inquiry.user_id == current_user.id,
        Payment.payment_status != "fully_paid"
    ).all()
    return jsonify([p.to_dict() for p in payments])

@payments_bp.route("/api/payments/<int:id>", methods=["PUT"])
@login_required
def update_payment(id):
    payment = Payment.query.join(Session).join(Inquiry).filter(
        Payment.id == id, Inquiry.user_id == current_user.id
    ).first_or_404()
    data = request.json or {}
    if "deposit_amount" in data:
        payment.deposit_amount = float(data["deposit_amount"])
    if "total_amount" in data:
        payment.total_amount = float(data["total_amount"])
    if payment.deposit_amount >= payment.total_amount and payment.total_amount > 0:
        payment.payment_status = "fully_paid"
    elif payment.deposit_amount > 0:
        payment.payment_status = "deposit_received"
    else:
        payment.payment_status = "deposit_pending"
    db.session.commit()
    return jsonify({"message": "Payment updated", "payment": payment.to_dict()})
