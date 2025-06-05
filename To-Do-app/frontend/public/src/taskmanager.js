export class TaskManager {
  constructor() {
    this.tasks = JSON.parse(localStorage.getItem("tasks")) || [];
  }

  addTask(text) {
    if (!text.trim()) return false;
    this.tasks.push({ text, completed: false });
    this._saveToStorage();
    return true;
  }

  deleteTask(index) {
    this.tasks.splice(index, 1);
    this._saveToStorage();
  }

  toggleComplete(index) {
    this.tasks[index].completed = !this.tasks[index].completed;
    this._saveToStorage();
  }

  _saveToStorage() {
    localStorage.setItem("tasks", JSON.stringify(this.tasks));
  }

  getTasks() {
    return this.tasks;
  }
}