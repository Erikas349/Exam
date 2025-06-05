import React, { useEffect, useState } from 'react';
import './App.css'; // Optional for styling

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch todos with error handling
  useEffect(() => {
    const fetchTodos = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`${API_URL}/todos`);
        if (!response.ok) throw new Error('Failed to fetch tasks');
        const data = await response.json();
        setTodos(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    fetchTodos();
  }, []);

  // Add todo with validation
  const addTodo = async () => {
    if (!newTask.trim()) {
      setError('Task cannot be empty');
      return;
    }

    try {
      const response = await fetch(`${API_URL}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: newTask }),
      });

      if (!response.ok) throw new Error('Failed to add task');
      
      const newTodo = await response.json();
      setTodos([...todos, { 
        id: newTodo.id, 
        task: newTask,
        done: false 
      }]);
      setNewTask('');
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  // Delete todo
  const deleteTodo = async (id) => {
    try {
      const response = await fetch(`${API_URL}/todos/${id}`, { 
        method: 'DELETE' 
      });
      if (!response.ok) throw new Error('Failed to delete task');
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="app-container">
      <h1>To-Do List</h1>
      
      {/* Error Display */}
      {error && <div className="error-message">{error}</div>}

      {/* Add Task Input */}
      <div className="input-container">
        <input
          type="text"
          value={newTask}
          placeholder="Enter a task..."
          onChange={(e) => {
            setNewTask(e.target.value);
            setError(null); // Clear error on typing
          }}
          onKeyPress={(e) => e.key === 'Enter' && addTodo()}
        />
        <button onClick={addTodo} disabled={isLoading}>
          {isLoading ? 'Adding...' : 'Add'}
        </button>
      </div>

      {/* Loading State */}
      {isLoading && <div>Loading tasks...</div>}

      {/* Todo List */}
      <ul className="todo-list">
        {todos.map(todo => (
          <li key={todo.id} className="todo-item">
            <span>{todo.task}</span>
            <button 
              onClick={() => deleteTodo(todo.id)}
              disabled={isLoading}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;