from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user
)

from models import db, User, Note
from forms import RegisterForm, LoginForm, NoteForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to continue.'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------- AUTH ROUTES ----------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'danger')
            return render_template('register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html', form=form)

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Account created. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ---------- CRUD ROUTES (Note) ----------

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    notes = Note.query.filter_by(user_id=current_user.id) \
        .order_by(Note.pinned.desc(), Note.updated_at.desc()).all()
    return render_template('dashboard.html', notes=notes)


@app.route('/note/new', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            pinned=form.pinned.data,
            user_id=current_user.id
        )
        db.session.add(note)
        db.session.commit()
        flash('Note saved.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('note_form.html', form=form, title='New Note')


@app.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        abort(403)

    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.category = form.category.data
        note.pinned = form.pinned.data
        db.session.commit()
        flash('Note updated.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('note_form.html', form=form, title='Edit Note')


@app.route('/note/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        abort(403)

    db.session.delete(note)
    db.session.commit()
    flash('Note deleted.', 'info')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # creates users.db + tables if they don't exist yet
    app.run(debug=True)
