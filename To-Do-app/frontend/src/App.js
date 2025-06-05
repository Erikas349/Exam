import React, { useEffect, useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';


function App() {
  const [todos, setTodos] = useState([]);
  const [newTask, setNewTask] = useState('');

  useEffect(() => {
    fetch(`${API_URL}/todos`)
      .then(res => res.json())
      .then(data => setTodos(data));
  }, []);

  const addTodo = () => {
    if (newTask.trim() === '') return;

    fetch(`${API_URL}/todos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task: newTask }),
    })
      .then(res => res.json())
      .then(data => {
        setTodos([...todos, { id: data.id || todos.length + 1, task: newTask }]);
        setNewTask('');
      });
  };

  const deleteTodo = (id) => {
    fetch(`${API_URL}/todos/${id}`, { method: 'DELETE' })
      .then(() => setTodos(todos.filter(todo => todo.id !== id)));
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>To-Do List</h1>

      <input
        type="text"
        value={newTask}
        placeholder="Enter a task..."
        onChange={(e) => setNewTask(e.target.value)}
      />
      <button onClick={addTodo} style={{ marginLeft: '10px' }}>Add</button>

      <ul>
        {todos.map(todo => (
          <li key={todo.id} style={{ marginTop: '10px' }}>
            {todo.task}
            <button onClick={() => deleteTodo(todo.id)} style={{ marginLeft: '10px' }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;