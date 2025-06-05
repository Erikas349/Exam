import React, { useEffect, useState } from 'react';

const BACKEND_URL = 'http://3.71.116.203:5000';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTask, setNewTask] = useState('');

  const fetchTodos = () => {
    fetch(`${BACKEND_URL}/todos`)
      .then(res => res.json())
      .then(data => setTodos(data));
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  const addTodo = () => {
    if (newTask.trim() === '') return;

    fetch(`${BACKEND_URL}/todos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task: newTask }),
    })
      .then(() => {
        setNewTask('');
        fetchTodos(); // Refresh list after adding
      });
  };

  const deleteTodo = (id) => {
    fetch(`${BACKEND_URL}/todos/${id}`, { method: 'DELETE' })
      .then(() => fetchTodos()); // Refresh list after deleting
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
