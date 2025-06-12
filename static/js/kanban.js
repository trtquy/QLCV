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
    
    // Initialize autocomplete functionality
    initializeAutocomplete();
    
    // Initialize feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Debug: Check if filterByTeam is accessible
    if (typeof window.filterByTeam === 'function') {
        console.log('filterByTeam function is available globally');
    } else {
        console.log('filterByTeam function is NOT available globally');
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
    console.log('Initializing task editing...');
    
    // Add click handlers for task cards (but not during drag)
    document.addEventListener('click', function(e) {
        console.log('Click detected:', e.target);
        
        // Check if clicked element is a button or inside a button
        if (e.target.closest('button') || e.target.closest('.time-tracking-btn')) {
            console.log('Button click, ignoring');
            return; // Don't trigger edit for button clicks
        }
        
        const taskCard = e.target.closest('.task-card');
        console.log('Task card found:', taskCard);
        
        if (taskCard && !taskCard.classList.contains('dragging')) {
            const taskId = taskCard.dataset.taskId;
            console.log('Task ID:', taskId);
            
            if (taskId) {
                console.log('Loading task for edit:', taskId);
                loadTaskForEdit(taskId);
            }
        }
    });
    
    // Add edit form submission handler
    const editForm = document.getElementById('editTaskForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Updating...';
            submitBtn.disabled = true;
        });
    }
    
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
    
    // Reset form when modal is hidden
    const editModal = document.getElementById('editTaskModal');
    if (editModal) {
        editModal.addEventListener('hidden.bs.modal', function() {
            const form = document.getElementById('editTaskForm');
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = 'Update Task';
                submitBtn.disabled = false;
            }
        });
    }
}

function loadTaskForEdit(taskId) {
    console.log('loadTaskForEdit called with ID:', taskId);
    console.log('Available task data:', window.tasksData);
    
    // Find task data
    const task = window.tasksData?.find(t => t.id == taskId);
    console.log('Found task:', task);
    
    if (!task) {
        console.error('Task not found:', taskId);
        alert('Task data not found. Please refresh the page.');
        return;
    }
    
    // Populate form fields
    document.getElementById('edit_title').value = task.title || '';
    document.getElementById('edit_description').value = task.description || '';
    document.getElementById('edit_assignee_id').value = task.assignee_id || '';
    document.getElementById('edit_priority').value = task.priority || 'medium';
    document.getElementById('edit_complexity').value = task.complexity || 'medium';
    document.getElementById('edit_status').value = task.status || 'todo';
    document.getElementById('edit_team_id').value = task.team_id || '';
    document.getElementById('edit_estimated_hours').value = task.estimated_hours || '';
    
    // Populate date fields
    document.getElementById('edit_started_at').value = task.started_at ? task.started_at.split('T')[0] : '';
    document.getElementById('edit_due_date').value = task.due_date ? task.due_date.split('T')[0] : '';
    document.getElementById('edit_completed_at').value = task.completed_at ? task.completed_at.split('T')[0] : '';
    
    // Set form action
    document.getElementById('editTaskForm').action = `/update_task/${taskId}`;
    
    console.log('Showing modal...');
    
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
    
    // Initialize "My Tasks" filter for analysts
    const myTasksFilter = document.getElementById('myTasksFilter');
    if (myTasksFilter) {
        myTasksFilter.addEventListener('change', function() {
            filterMyTasks(this.value);
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

function filterMyTasks(filterValue) {
    const taskCards = document.querySelectorAll('.task-card');
    const currentUserId = window.currentUserId; // This will be set from the template
    
    taskCards.forEach(card => {
        if (filterValue === 'my-tasks') {
            // Show only tasks assigned to current user
            const assigneeId = card.dataset.assigneeId;
            if (assigneeId && assigneeId === currentUserId) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        } else {
            // Show all tasks
            card.style.display = '';
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
            startTimer(taskId);
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
            // Stop all timers
            if (window.timeTrackingIntervals) {
                Object.keys(window.timeTrackingIntervals).forEach(taskId => {
                    stopTimer(taskId);
                });
            }
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

function startTimer(taskId) {
    // Start visual timer
    const btn = document.getElementById(`time-btn-${taskId}`);
    const icon = document.getElementById(`time-icon-${taskId}`);
    const duration = document.getElementById(`time-duration-${taskId}`);
    
    if (btn && icon && duration) {
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-success');
        icon.setAttribute('data-feather', 'stop-circle');
        duration.style.display = 'inline';
        
        // Refresh feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
        
        // Start timer interval
        window.timeTrackingIntervals = window.timeTrackingIntervals || {};
        const startTime = new Date();
        
        window.timeTrackingIntervals[taskId] = setInterval(() => {
            const elapsed = Math.floor((new Date() - startTime) / 1000);
            const hours = Math.floor(elapsed / 3600);
            const minutes = Math.floor((elapsed % 3600) / 60);
            const seconds = elapsed % 60;
            
            if (hours > 0) {
                duration.textContent = `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            } else {
                duration.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            }
        }, 1000);
    }
}

function stopTimer(taskId) {
    // Stop visual timer
    const btn = document.getElementById(`time-btn-${taskId}`);
    const icon = document.getElementById(`time-icon-${taskId}`);
    const duration = document.getElementById(`time-duration-${taskId}`);
    
    if (btn && icon && duration) {
        btn.classList.remove('btn-success');
        btn.classList.add('btn-outline-primary');
        icon.setAttribute('data-feather', 'play');
        duration.style.display = 'none';
        duration.textContent = '';
        
        // Refresh feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
        
        // Clear timer interval
        if (window.timeTrackingIntervals && window.timeTrackingIntervals[taskId]) {
            clearInterval(window.timeTrackingIntervals[taskId]);
            delete window.timeTrackingIntervals[taskId];
        }
    }
}

// Export functions for global use
window.loadTaskForEdit = loadTaskForEdit;
window.updateTaskStatus = updateTaskStatus;
window.showNotification = showNotification;
window.refreshIcons = refreshIcons;
window.toggleTimeTracking = toggleTimeTracking;
window.updateTaskEstimate = updateTaskEstimate;
