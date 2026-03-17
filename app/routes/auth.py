from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/login")
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))
    return render_template("login.html")

@auth_bp.route("/register")
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))
    return render_template("register.html")

@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json or {}
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400
    user = User(email=data["email"], studio_name=data.get("studio_name", ""))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    user = User.query.filter_by(email=data.get("email")).first()
    if user and user.check_password(data.get("password", "")):
        login_user(user)
        return jsonify({"message": "Logged in", "studio_name": user.studio_name or user.email})
    return jsonify({"error": "Invalid email or password"}), 401

@auth_bp.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})
