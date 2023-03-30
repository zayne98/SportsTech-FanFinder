import React, { useState } from 'react';
import { saveAs } from 'file-saver';

function App() {
  const [newTodo, setNewTodo] = useState('');
  const [todos, setTodos] = useState([]);

  const handleAddTodo = () => {
    if (newTodo.trim()) {
      setTodos([...todos, newTodo]);
      setNewTodo('');
    }
  };

  const handleDeleteTodo = (index) => {
    setTodos([...todos.slice(0, index), ...todos.slice(index + 1)]);
  };

  const handleExportTxt = () => {
    const blob = new Blob([todos.join('\n')], { type: 'text/plain;charset=utf-8' });
    saveAs(blob, 'gps_data.csv');
  };

  return (
    <div className="container">
      <h1>Todo List</h1>
      <div>
        <input type="text" value={newTodo} onChange={(e) => setNewTodo(e.target.value)} placeholder="Add new item" />
        <button onClick={handleAddTodo}>Add</button>
      </div>
      <ul>
        {todos.map((todo, index) => (
          <li key={index}>
            <span>{todo}</span>
            <button onClick={() => handleDeleteTodo(index)}>X</button>
          </li>
        ))}
      </ul>
      <button onClick={handleExportTxt}>Export to TXT</button>
    </div>
  );
}

export default App;

