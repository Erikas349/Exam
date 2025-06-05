// js/main.js
import { TaskManager } from './taskManager.js';

const taskInput = document.getElementById("taskInput");
const addTaskBtn = document.getElementById("addTaskBtn");
const taskList = document.getElementById("taskList");

const manager = new TaskManager();

function renderTasks() {
  taskList.innerHTML = manager.getTasks().map((task, index) => `
    <li class="${task.completed ? 'completed' : ''}">
      ${task.text}
      <button onclick="deleteTask(${index})">Delete</button>
    </li>
  `).join("");
}

// Event Listeners
addTaskBtn.addEventListener("click", () => {
  if (manager.addTask(taskInput.value)) {
    taskInput.value = "";
    renderTasks();
  }
});

// Expose to global scope for HTML `onclick` (or use event delegation)
window.deleteTask = (index) => {
  manager.deleteTask(index);
  renderTasks();
};