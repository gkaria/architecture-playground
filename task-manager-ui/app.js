/**
 * Task Manager UI - JavaScript Application
 * Interacts with different architecture pattern backends
 */

// Configuration
const ARCHITECTURES = {
    monolith: { port: 8001, color: 'blue', name: 'Monolithic' },
    'modular-monolith': { port: 8002, color: 'green', name: 'Modular Monolith' },
    microservices: { port: 8003, color: 'purple', name: 'Microservices' },
    'event-driven': { port: 8004, color: 'red', name: 'Event-Driven' },
    layered: { port: 8005, color: 'yellow', name: 'Layered' },
    'service-based': { port: 8006, color: 'indigo', name: 'Service-Based' }
};

// State
let currentArchitecture = 'monolith';
let currentFilter = 'all';
let tasks = [];

// Get API base URL
function getApiUrl() {
    const arch = ARCHITECTURES[currentArchitecture];
    return `http://localhost:${arch.port}`;
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadTasks();
});

// Initialize event listeners
function initializeEventListeners() {
    // Architecture selector
    document.getElementById('architecture-selector').addEventListener('change', (e) => {
        currentArchitecture = e.target.value;
        showToast(`Switched to ${ARCHITECTURES[currentArchitecture].name} architecture`);
        loadTasks();
    });

    // Create task form
    document.getElementById('create-task-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await createTask();
    });

    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', () => {
        loadTasks();
    });

    // Filter tabs
    document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            currentFilter = e.target.dataset.filter;
            updateFilterTabs();
            renderTasks();
        });
    });
}

// Update filter tab styles
function updateFilterTabs() {
    document.querySelectorAll('.filter-tab').forEach(tab => {
        if (tab.dataset.filter === currentFilter) {
            tab.classList.add('active', 'border-blue-600', 'text-blue-600');
            tab.classList.remove('border-transparent', 'text-gray-500');
        } else {
            tab.classList.remove('active', 'border-blue-600', 'text-blue-600');
            tab.classList.add('border-transparent', 'text-gray-500');
        }
    });
}

// Load tasks from API
async function loadTasks() {
    showLoading();
    const startTime = performance.now();

    try {
        const response = await fetch(`${getApiUrl()}/tasks`);
        const endTime = performance.now();
        const responseTime = Math.round(endTime - startTime);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        tasks = await response.json();

        // Update response time
        document.getElementById('response-time').textContent = `${responseTime}ms`;

        renderTasks();
        updateStats();
        hideError();
    } catch (error) {
        console.error('Failed to load tasks:', error);
        showError(`Failed to connect to ${ARCHITECTURES[currentArchitecture].name} API (Port ${ARCHITECTURES[currentArchitecture].port}). Make sure the backend is running.`);
        document.getElementById('response-time').textContent = '-';
    } finally {
        hideLoading();
    }
}

// Create a new task
async function createTask() {
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-description').value;
    const priority = document.getElementById('task-priority').value;
    const tagsInput = document.getElementById('task-tags').value;
    const tags = tagsInput ? tagsInput.split(',').map(t => t.trim()).filter(t => t) : [];

    const taskData = {
        title,
        description,
        priority,
        tags,
        user_id: 1,  // Default user
        project_id: 1,  // Default project
        status: 'todo'
    };

    const btn = document.getElementById('create-task-btn');
    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div><span>Creating...</span>';

    const startTime = performance.now();

    try {
        const response = await fetch(`${getApiUrl()}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });

        const endTime = performance.now();
        const responseTime = Math.round(endTime - startTime);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const newTask = await response.json();

        // Reset form
        document.getElementById('create-task-form').reset();

        // Show success message
        showToast(`Task created successfully in ${responseTime}ms`);

        // Reload tasks
        await loadTasks();
    } catch (error) {
        console.error('Failed to create task:', error);
        showToast(`Failed to create task: ${error.message}`, true);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span>Create Task</span>';
    }
}

// Update task status
async function updateTaskStatus(taskId, newStatus) {
    const startTime = performance.now();

    try {
        const response = await fetch(`${getApiUrl()}/tasks/${taskId}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus })
        });

        const endTime = performance.now();
        const responseTime = Math.round(endTime - startTime);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        showToast(`Status updated in ${responseTime}ms`);
        await loadTasks();
    } catch (error) {
        console.error('Failed to update task:', error);
        showToast(`Failed to update task: ${error.message}`, true);
    }
}

// Delete task
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    const startTime = performance.now();

    try {
        const response = await fetch(`${getApiUrl()}/tasks/${taskId}`, {
            method: 'DELETE'
        });

        const endTime = performance.now();
        const responseTime = Math.round(endTime - startTime);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        showToast(`Task deleted in ${responseTime}ms`);
        await loadTasks();
    } catch (error) {
        console.error('Failed to delete task:', error);
        showToast(`Failed to delete task: ${error.message}`, true);
    }
}

// Render tasks in the UI
function renderTasks() {
    const taskList = document.getElementById('task-list');
    const emptyState = document.getElementById('empty-state');

    // Filter tasks
    let filteredTasks = tasks;
    if (currentFilter !== 'all') {
        filteredTasks = tasks.filter(task => task.status === currentFilter);
    }

    // Show empty state if no tasks
    if (filteredTasks.length === 0) {
        taskList.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
    }

    emptyState.classList.add('hidden');

    // Render tasks
    taskList.innerHTML = filteredTasks.map(task => createTaskCard(task)).join('');

    // Attach event listeners to status buttons and delete buttons
    filteredTasks.forEach(task => {
        const statusSelect = document.getElementById(`status-${task.id}`);
        if (statusSelect) {
            statusSelect.addEventListener('change', (e) => {
                updateTaskStatus(task.id, e.target.value);
            });
        }

        const deleteBtn = document.getElementById(`delete-${task.id}`);
        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => {
                deleteTask(task.id);
            });
        }
    });
}

// Create task card HTML
function createTaskCard(task) {
    const statusColors = {
        todo: 'bg-gray-100 text-gray-700',
        in_progress: 'bg-yellow-100 text-yellow-700',
        done: 'bg-green-100 text-green-700'
    };

    const priorityColors = {
        low: 'bg-blue-100 text-blue-700',
        medium: 'bg-yellow-100 text-yellow-700',
        high: 'bg-red-100 text-red-700'
    };

    const statusLabels = {
        todo: 'To Do',
        in_progress: 'In Progress',
        done: 'Done'
    };

    return `
        <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition fade-in">
            <div class="flex justify-between items-start mb-2">
                <div class="flex-1">
                    <h4 class="font-semibold text-gray-900 mb-1">${escapeHtml(task.title)}</h4>
                    <p class="text-sm text-gray-600 mb-2">${escapeHtml(task.description)}</p>
                </div>
                <button
                    id="delete-${task.id}"
                    class="text-gray-400 hover:text-red-600 ml-2"
                    title="Delete task"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                </button>
            </div>

            <div class="flex flex-wrap items-center gap-2 mb-3">
                <span class="px-2 py-1 rounded text-xs font-medium ${priorityColors[task.priority]}">
                    ${task.priority.toUpperCase()}
                </span>
                ${task.tags && task.tags.length > 0 ? task.tags.map(tag => `
                    <span class="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                        ${escapeHtml(tag)}
                    </span>
                `).join('') : ''}
            </div>

            <div class="flex items-center justify-between pt-3 border-t border-gray-100">
                <div class="flex items-center gap-2">
                    <label for="status-${task.id}" class="text-xs font-medium text-gray-500">Status:</label>
                    <select
                        id="status-${task.id}"
                        class="text-xs px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 ${statusColors[task.status]}"
                    >
                        <option value="todo" ${task.status === 'todo' ? 'selected' : ''}>To Do</option>
                        <option value="in_progress" ${task.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                        <option value="done" ${task.status === 'done' ? 'selected' : ''}>Done</option>
                    </select>
                </div>
                <div class="text-xs text-gray-400">
                    ID: ${task.id}
                </div>
            </div>
        </div>
    `;
}

// Update statistics
function updateStats() {
    const total = tasks.length;
    const inProgress = tasks.filter(t => t.status === 'in_progress').length;
    const done = tasks.filter(t => t.status === 'done').length;

    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-progress').textContent = inProgress;
    document.getElementById('stat-done').textContent = done;
}

// Show loading state
function showLoading() {
    document.getElementById('loading-state').classList.remove('hidden');
    document.getElementById('task-list').classList.add('hidden');
    document.getElementById('empty-state').classList.add('hidden');
}

// Hide loading state
function hideLoading() {
    document.getElementById('loading-state').classList.add('hidden');
    document.getElementById('task-list').classList.remove('hidden');
}

// Show error state
function showError(message) {
    document.getElementById('error-state').classList.remove('hidden');
    document.getElementById('error-message').textContent = message;
    document.getElementById('task-list').classList.add('hidden');
    document.getElementById('empty-state').classList.add('hidden');
}

// Hide error state
function hideError() {
    document.getElementById('error-state').classList.add('hidden');
}

// Show toast notification
function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');

    toastMessage.textContent = message;

    if (isError) {
        toast.classList.add('bg-red-600');
        toast.classList.remove('bg-gray-900');
    } else {
        toast.classList.add('bg-gray-900');
        toast.classList.remove('bg-red-600');
    }

    toast.classList.remove('hidden');

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
