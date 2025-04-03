from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime
app = Flask(__name__)

# データベースの初期化
def init_db():
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS task (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        memo TEXT NOT NULL,
                        deadline TEXT,
                        important INTEGER DEFAULT 0,
                        created_at TEXT DEFAULT (datetime('now', 'localtime')),
                        updated_at TEXT,
                        position INTEGER  DEFAULT 0,
                        completed_at TEXT)''')
        conn.commit()

# タスク一覧表示
@app.route('/')
def index():
    with sqlite3.connect('todo.db') as conn:        
        conn.row_factory = sqlite3.Row  #フィールド名で値を取得できるようにする
        c = conn.cursor()
        c.execute('SELECT id, title, deadline, completed_at,important FROM task ORDER BY position,important ASC,deadline ASC')
        tasks = c.fetchall()
    return render_template('index.html', tasks=tasks)

# タスク登録画面
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        memo = request.form['memo']
        deadline = request.form['deadline']
        important = request.form.get('important', '0') 
        print('important' + important)

        with sqlite3.connect('todo.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO task (title, memo, deadline, important) VALUES (?, ?, ?, ?)', (title, memo, deadline, important))
            conn.commit()
        return redirect('/')
    # GETの場合、現在の日付を取得（例: 2025-04-03 形式）
    current_date = datetime.now().strftime("%Y-%m-%d")
    return render_template('add.html', current_date=current_date)

# タスク編集画面
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        if request.method == 'POST':
            title = request.form['title']
            memo = request.form['memo']
            deadline = request.form['deadline']
            important = request.form.get('important', '0') 
            c.execute('UPDATE task SET title=?, memo=?, deadline=?, important=?,updated_at=datetime("now", "localtime") WHERE id=?',
                      (title, memo, deadline, important,task_id))
            conn.commit()
            return redirect('/')
        conn.row_factory = sqlite3.Row  
        c.execute('SELECT id, title, memo, deadline, important, completed_at FROM task WHERE id=?', (task_id,))
        task = c.fetchone()
    return render_template('edit.html', task=task)

# タスク順番更新API
@app.route('/update_order', methods=['POST'])
def update_order():
    order = request.json['order']
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        for index, task in enumerate(order):
            c.execute('UPDATE task SET position=? WHERE id=?', (index + 1, task['id']))
        conn.commit()
    return jsonify({'status': 'success'})

# タスク削除API
@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM task WHERE id=?', (task_id,))
        conn.commit()
    return jsonify({'status': 'success'})

# 完了したタスクを削除するAPI
@app.route('/delete_completed_tasks', methods=['DELETE'])
def delete_completed_tasks():
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM task WHERE completed_at IS NOT NULL')
        conn.commit()
    return jsonify({'status': 'success'})

# タスクを完了にするAPI
@app.route('/complete_task', methods=['POST'])
def complete_task():
    task_id = request.json['task_id']
    completed = request.json['completed']

    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        if completed:
            completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute('UPDATE task SET completed_at=? WHERE id=?', (completed_at, task_id))
        else:
            c.execute('UPDATE task SET completed_at=NULL WHERE id=?', (task_id,))
        conn.commit()
    return jsonify({'status': 'success'})

# タスクを完了にするAPI
@app.route('/complete', methods=['POST'])
def complete():
    task_id = request.form['task_id']
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('UPDATE task SET completed_at=? WHERE id=?', (completed_at, task_id))
        conn.commit()
    return redirect('/')
    
# 404エラーハンドラー
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
