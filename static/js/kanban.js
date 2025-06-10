// Kanban Board JavaScript

let draggedTask = null;

function initializeKanban() {
    console.log('Initializing Kanban board...');
    
    // Add drag and drop event listeners
    initializeDragAndDrop();
    
    // Add task editing functionality
    initializeTaskEditing();
    
    // Add time tracking functionality
    initializeTimeTracking();
    
    // Initialize feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function initializeDragAndDrop() {
    const taskCards = document.querySelectorAll('.task-card');
    const kanbanColumns = document.querySelectorAll('.kanban-column');
    
    // Add drag events to task cards
    taskCards.forEach(card => {
        card.addEventListener('dragstart', handleDragStart);
        card.addEventListener('dragend', handleDragEnd);
    });
    
    // Add drop events to columns
    kanbanColumns.forEach(column => {
        column.addEventListener('dragover', handleDragOver);
        column.addEventListener('drop', handleDrop);
        column.addEventListener('dragenter', handleDragEnter);
        column.addEventListener('dragleave', handleDragLeave);
    });
}

function handleDragStart(e) {
    draggedTask = this;
    this.classList.add('dragging');
    
    // Store task data
    e.dataTransfer.setData('text/plain', this.dataset.taskId);
    e.dataTransfer.effectAllowed = 'move';
    
    console.log('Drag started for task:', this.dataset.taskId);
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
    draggedTask = null;
    
    // Remove drag-over effects from all columns
    document.querySelectorAll('.kanban-column').forEach(column => {
        column.classList.remove('drag-over');
    });
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
}

function handleDragEnter(e) {
    e.preventDefault();
    this.classList.add('drag-over');
}

function handleDragLeave(e) {
    // Only remove if leaving the column entirely
    if (!this.contains(e.relatedTarget)) {
        this.classList.remove('drag-over');
    }
}

function handleDrop(e) {
    e.preventDefault();
    this.classList.remove('drag-over');
    
    const taskId = e.dataTransfer.getData('text/plain');
    const newStatus = this.dataset.status;
    
    if (draggedTask && taskId) {
        updateTaskStatus(taskId, newStatus);
    }
}

function updateTaskStatus(taskId, newStatus) {
    console.log('Updating task status:', taskId, newStatus);
    
    // Show loading state
    const taskCard = document.querySelector(`[data-task-id="${taskId}"]`);
    if (taskCard) {
        taskCard.classList.add('loading');
    }
    
    // Create form data
    const formData = new FormData();
    formData.append('status', newStatus);
    
    // Send update request
    fetch(`/update_task/${taskId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Task status updated successfully');
            
            // Move the task card to the new column
            const newColumn = document.querySelector(`[data-status="${newStatus}"] .task-container`);
            if (newColumn && taskCard) {
                newColumn.appendChild(taskCard);
                updateColumnCounts();
                showNotification('Task status updated successfully!', 'success');
            }
        } else {
            console.error('Failed to update task status:', data.error);
            showNotification('Failed to update task status', 'error');
        }
    })
    .catch(error => {
        console.error('Error updating task status:', error);
        showNotification('Error updating task status', 'error');
    })
    .finally(() => {
        if (taskCard) {
            taskCard.classList.remove('loading');
        }
    });
}

function initializeTaskEditing() {
    // Add click handlers for task cards (but not during drag)
    document.addEventListener('click', function(e) {
        const taskCard = e.target.closest('.task-card');
        if (taskCard && !taskCard.classList.contains('dragging')) {
            const taskId = taskCard.dataset.taskId;
            loadTaskForEdit(taskId);
        }
    });
    
    // Add delete button handler
    const deleteBtn = document.getElementById('deleteTaskBtn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function() {
            const form = document.getElementById('editTaskForm');
            if (form && confirm('Are you sure you want to delete this task?')) {
                const taskId = form.action.split('/').pop();
                deleteTask(taskId);
            }
        });
    }
}

function loadTaskForEdit(taskId) {
    // Find task data
    const task = window.tasksData?.find(t => t.id === taskId);
    if (!task) {
        console.error('Task not found:', taskId);
        return;
    }
    
    // Populate form fields
    document.getElementById('edit_title').value = task.title || '';
    document.getElementById('edit_description').value = task.description || '';
    document.getElementById('edit_assignee_id').value = task.assignee_id || '';
    document.getElementById('edit_priority').value = task.priority || 'medium';
    document.getElementById('edit_status').value = task.status || 'todo';
    
    // Set form action
    document.getElementById('editTaskForm').action = `/update_task/${taskId}`;
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('editTaskModal'));
    modal.show();
}

function deleteTask(taskId) {
    // Create form and submit
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/delete_task/${taskId}`;
    
    document.body.appendChild(form);
    form.submit();
}

function updateColumnCounts() {
    // Update badge counts for each column
    const columns = ['todo', 'in_progress', 'completed'];
    
    columns.forEach(status => {
        const column = document.querySelector(`[data-status="${status}"]`);
        const badge = column?.querySelector('.badge');
        const taskCount = column?.querySelectorAll('.task-card').length || 0;
        
        if (badge) {
            badge.textContent = taskCount;
        }
    });
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 80px; right: 20px; z-index: 9999; max-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 3000);
}

// Search and filter functionality
function initializeSearch() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    
    if (searchForm && searchInput) {
        // Add debounced search
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterTasks(this.value);
            }, 300);
        });
    }
}

function filterTasks(query) {
    const taskCards = document.querySelectorAll('.task-card');
    const lowerQuery = query.toLowerCase();
    
    taskCards.forEach(card => {
        const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
        const description = card.querySelector('.card-text')?.textContent.toLowerCase() || '';
        
        if (title.includes(lowerQuery) || description.includes(lowerQuery) || !query) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
    
    updateColumnCounts();
}

// Mobile touch support
function initializeTouchSupport() {
    let touchStartY = 0;
    let touchStartX = 0;
    let isDragging = false;
    
    document.addEventListener('touchstart', function(e) {
        const taskCard = e.target.closest('.task-card');
        if (taskCard) {
            touchStartY = e.touches[0].clientY;
            touchStartX = e.touches[0].clientX;
            isDragging = false;
        }
    });
    
    document.addEventListener('touchmove', function(e) {
        if (Math.abs(e.touches[0].clientY - touchStartY) > 10 || 
            Math.abs(e.touches[0].clientX - touchStartX) > 10) {
            isDragging = true;
        }
    });
    
    document.addEventListener('touchend', function(e) {
        const taskCard = e.target.closest('.task-card');
        if (taskCard && !isDragging) {
            // Treat as click on mobile
            const taskId = taskCard.dataset.taskId;
            loadTaskForEdit(taskId);
        }
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeKanban();
    initializeSearch();
    initializeTouchSupport();
});

// Refresh icons after dynamic content changes
function refreshIcons() {
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

// Time tracking functionality
let activeTimeLog = null;

function initializeTimeTracking() {
    // Check for active time tracking on page load
    checkActiveTimeLog();
    
    // Set up periodic checks
    setInterval(checkActiveTimeLog, 30000); // Check every 30 seconds
}

function checkActiveTimeLog() {
    fetch('/time/active')
        .then(response => response.json())
        .then(data => {
            if (data.active) {
                activeTimeLog = data.time_log;
                updateTimeTrackingUI();
            } else {
                activeTimeLog = null;
                updateTimeTrackingUI();
            }
        })
        .catch(error => console.error('Error checking active time log:', error));
}

function toggleTimeTracking(taskId) {
    if (activeTimeLog && activeTimeLog.task_id === taskId) {
        // Stop tracking
        stopTimeTracking(activeTimeLog.id);
    } else if (activeTimeLog) {
        // Already tracking another task - confirm switch
        if (confirm('You are already tracking time on another task. Switch to this task?')) {
            stopTimeTracking(activeTimeLog.id, () => {
                startTimeTracking(taskId);
            });
        }
    } else {
        // Start tracking
        startTimeTracking(taskId);
    }
}

function startTimeTracking(taskId) {
    const formData = new FormData();
    formData.append('description', '');
    
    fetch(`/time/start/${taskId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            checkActiveTimeLog();
        } else {
            showNotification(data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error starting time tracking:', error);
        showNotification('Failed to start time tracking', 'error');
    });
}

function stopTimeTracking(timeLogId, callback = null) {
    fetch(`/time/stop/${timeLogId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            activeTimeLog = null;
            updateTimeTrackingUI();
            if (callback) callback();
        } else {
            showNotification(data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error stopping time tracking:', error);
        showNotification('Failed to stop time tracking', 'error');
    });
}

function updateTimeTrackingUI() {
    const timeButtons = document.querySelectorAll('.time-tracking-btn');
    
    timeButtons.forEach(button => {
        const taskId = button.dataset.taskId;
        const icon = button.querySelector('i');
        
        if (activeTimeLog && activeTimeLog.task_id === taskId) {
            // This task is being tracked
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-danger');
            icon.setAttribute('data-feather', 'stop-circle');
            button.title = 'Stop time tracking';
        } else {
            // This task is not being tracked
            button.classList.remove('btn-danger');
            button.classList.add('btn-outline-primary');
            icon.setAttribute('data-feather', 'play');
            button.title = 'Start time tracking';
        }
    });
    
    // Refresh icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function updateTaskEstimate(taskId, estimatedHours) {
    const formData = new FormData();
    formData.append('estimated_hours', estimatedHours);
    
    fetch(`/task/estimate/${taskId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
        } else {
            showNotification(data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error updating task estimate:', error);
        showNotification('Failed to update estimate', 'error');
    });
}

// Export functions for global use
window.loadTaskForEdit = loadTaskForEdit;
window.updateTaskStatus = updateTaskStatus;
window.showNotification = showNotification;
window.refreshIcons = refreshIcons;
window.toggleTimeTracking = toggleTimeTracking;
window.updateTaskEstimate = updateTaskEstimate;
