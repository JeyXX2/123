import os
import uuid

from flask import Blueprint, flash, jsonify, redirect, render_template, send_from_directory, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename

from .extensions import db
from .forms import LoginForm, NoteForm, RegistrationForm, UploadForm, EditProfileForm
from .models import Note, User, UserFile


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data.lower()).first()
        if existing_user:
            flash("Пользователь с таким email уже существует", "warning")
            return redirect(url_for("main.register"))

        user = User(username=form.username.data.strip(), email=form.email.data.lower().strip())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Регистрация успешна, теперь войдите", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вы вошли в систему", "success")
            return redirect(url_for("main.dashboard"))

        flash("Неверный email или пароль", "danger")

    return render_template("login.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for("main.index"))


@main_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    note_form = NoteForm(prefix="note")
    upload_form = UploadForm(prefix="upload")

    if note_form.submit.data and note_form.validate_on_submit():
        note = Note(title=note_form.title.data.strip(), content=note_form.content.data.strip(), author=current_user)
        db.session.add(note)
        db.session.commit()
        flash("Заметка добавлена", "success")
        return redirect(url_for("main.dashboard"))

    if upload_form.submit.data and upload_form.validate_on_submit():
        incoming_file = upload_form.file.data
        original_name = secure_filename(incoming_file.filename)
        unique_name = f"{uuid.uuid4().hex}_{original_name}"
        save_path = os.path.join(main_bp.root_path, "uploads", unique_name)
        incoming_file.save(save_path)

        record = UserFile(original_name=original_name, stored_name=unique_name, owner=current_user)
        db.session.add(record)
        db.session.commit()
        flash("Файл загружен", "success")
        return redirect(url_for("main.dashboard"))

    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).all()
    files = UserFile.query.filter_by(user_id=current_user.id).order_by(UserFile.uploaded_at.desc()).all()

    return render_template("dashboard.html", note_form=note_form, upload_form=upload_form, notes=notes, files=files)


@main_bp.route("/api/my-notes", methods=["GET"])
@login_required
def my_notes_api():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).all()
    payload = [
        {"id": n.id, "title": n.title, "content": n.content, "created_at": n.created_at.isoformat()} for n in notes
    ]
    return jsonify({"user": current_user.email, "notes": payload, "count": len(payload)})


@main_bp.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id: int):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    flash("Заметка удалена", "info")
    return redirect(url_for("main.dashboard"))


@main_bp.route("/files/<int:file_id>/download", methods=["GET"])
@login_required
def download_file(file_id: int):
    user_file = UserFile.query.filter_by(id=file_id, user_id=current_user.id).first_or_404()
    upload_dir = os.path.join(main_bp.root_path, "uploads")
    return send_from_directory(upload_dir, user_file.stored_name, as_attachment=True, download_name=user_file.original_name)


@main_bp.route("/files/<int:file_id>/delete", methods=["POST"])
@login_required
def delete_file(file_id: int):
    user_file = UserFile.query.filter_by(id=file_id, user_id=current_user.id).first_or_404()
    upload_dir = os.path.join(main_bp.root_path, "uploads")
    file_path = os.path.join(upload_dir, user_file.stored_name)

    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(user_file)
    db.session.commit()
    flash("Файл удален", "info")
    return redirect(url_for("main.dashboard"))


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@main_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('edit_profile.html', form=form)
