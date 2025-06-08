from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Путь к файлу для хранения задач
TODOS_FILE = 'todos.json'

def load_todos():
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(load_todos())

@app.route('/api/todos', methods=['POST'])
def add_todo():
    todos = load_todos()
    data = request.get_json()
    new_todo = {
        'id': data.get('id'),
        'text': data.get('text'),
        'completed': False
    }
    todos.append(new_todo)
    save_todos(todos)
    return jsonify(new_todo)

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todos = load_todos()
    data = request.get_json()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = data.get('completed', todo['completed'])
            todo['text'] = data.get('text', todo['text'])
            save_todos(todos)
            return jsonify(todo)
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = load_todos()
    todos = [todo for todo in todos if todo['id'] != todo_id]
    save_todos(todos)
    return jsonify({'message': 'Todo deleted'})

if __name__ == '__main__':
    app.run(debug=True) 