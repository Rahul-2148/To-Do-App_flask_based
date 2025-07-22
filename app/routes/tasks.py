from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Task
from flask_login import current_user, login_required

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('tasks.tasks'))
    return render_template('home.html')

@tasks_bp.route('/tasks', methods=['GET'])
@login_required
def tasks():
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    theme = session.get('theme', 'theme-light')
    return render_template("tasks.html", theme=theme, tasks=user_tasks)

@tasks_bp.route('/add-task', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    new_task = Task(title=title, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    flash('✅ Task added!', 'success')
    return redirect(url_for('tasks.tasks'))

@tasks_bp.route('/toggle-status/<int:task_id>', methods=['POST'])
@login_required
def toggle_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.status == 'pending':
        task.status = 'working'
    elif task.status == 'working':
        task.status = 'done'
    else:
        task.status = 'pending'
    db.session.commit()
    return redirect(url_for('tasks.tasks'))

@tasks_bp.route('/clear-task', methods=['POST'])
@login_required
def clear_task():
    Task.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('🧹 All tasks cleared.', 'warning')
    return redirect(url_for('tasks.tasks'))

@tasks_bp.route('/delete-selected', methods=['POST'])
@login_required
def delete_selected():
    ids = request.form.getlist('selected_tasks')
    if ids:
        Task.query.filter(Task.id.in_(ids), Task.user_id == current_user.id).delete(synchronize_session=False)
        db.session.commit()
        flash(f'🗑️ Deleted {len(ids)} selected task(s).', 'danger')
    else:
        flash('⚠️ No tasks selected for deletion.', 'warning')
    return redirect(url_for('tasks.tasks'))

@tasks_bp.route('/set-theme/<theme>', methods=['GET'])
def set_theme(theme):
    session['theme'] = theme
    return '', 204
