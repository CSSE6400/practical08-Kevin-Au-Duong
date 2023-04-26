from flask import Blueprint, jsonify, request 
from todo.models import db 
from todo.models.todo import Todo 
from datetime import datetime, timedelta

api = Blueprint('api', __name__, url_prefix='/api/v1') 


@api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})


@api.route('/todos', methods=['GET'])
def get_todos():
    """Return the list of todo items"""
    completed = request.args.get('completed')
    window = request.args.get('window')

    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    result = []
    for todo in todos:

        if completed is not None:
            if str(todo.completed).lower() != completed:
                continue

        if window is not None:
            date_limit = datetime.utcnow() + timedelta(days=int(window))
            if todo.deadline_at > date_limit:
                continue

        result.append(todo.to_dict())
    return jsonify(result)

@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Return the details of a todo item"""
    todo = Todo.query.get(todo_id) 
    if todo is None: 
        return jsonify({'error': 'Todo not found'}), 404 
    return jsonify(todo.to_dict())

@api.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo item and return the created item"""
    if not set(request.json.keys()).issubset(set(('title', 'description', 'completed', 'deadline_at'))):
        return jsonify({'error': 'extra fields'}), 400

    if "title" not in request.json:
        return jsonify({'error': 'missing title'}), 400

    todo = Todo( 
        title=request.json.get('title'), 
        description=request.json.get('description'), 
        completed=request.json.get('completed', False), 
    ) 
    if 'deadline_at' in request.json: 
        todo.deadline_at = datetime.fromisoformat(request.json.get('deadline_at')) 

    # Adds a new record to the database or will update an existing record 
    db.session.add(todo) 
    # Commits the changes to the database, this must be called for the changes to be saved 
    db.session.commit() 
    return jsonify(todo.to_dict()), 201

@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo item and return the updated item"""
    if not set(request.json.keys()).issubset(set(('title', 'description', 'completed', 'deadline_at'))):
        return jsonify({'error': 'extra fields'}), 400

    todo = Todo.query.get(todo_id) 
    if todo is None: 
        return jsonify({'error': 'Todo not found'}), 404 
    
    todo.title = request.json.get('title', todo.title) 
    todo.description = request.json.get('description', todo.description) 
    todo.completed = request.json.get('completed', todo.completed) 
    todo.deadline_at = request.json.get('deadline_at', todo.deadline_at) 
    db.session.commit() 
    
    return jsonify(todo.to_dict())

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo item and return the deleted item"""
    todo = Todo.query.get(todo_id) 
    if todo is None: 
        return jsonify({}), 200 

    db.session.delete(todo) 
    db.session.commit() 
    return jsonify(todo.to_dict()), 200
 
