from flask import Flask, render_template, request, redirect, url_for, jsonify

class Task:
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

app = Flask(__name__)

tasks = []

def load_tasks():
    global tasks
    tasks = []
    with open('tasks.txt', 'r') as file:
        for line in file:
            title, completed = line.strip().split(',')
            task = Task(title, completed=bool(int(completed)))
            tasks.append(task)

def save_tasks():
    with open('tasks.txt', 'w') as file:
        for task in tasks:
            completed = int(task.completed)
            file.write(f"{task.title},{completed}\n")

load_tasks()

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    task = Task(title)
    tasks.append(task)
    save_tasks()
    return redirect(url_for('index'))

@app.route('/toggle_task/<int:task_index>')
def toggle_task(task_index):
    if task_index < len(tasks):
        task = tasks[task_index]
        task.completed = not task.completed
        save_tasks()  
        return jsonify({'completed': task.completed})
    else:
        return jsonify({'error': 'Invalid task index'})

@app.route('/remove/<int:task_index>')
def remove_task(task_index):
    if task_index < len(tasks):
        tasks.pop(task_index)
        save_tasks()  
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
