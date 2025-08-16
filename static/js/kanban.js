// Kanban Board JavaScript

let draggedTask = null;

function initializeKanban() {
    console.log('Initializing Kanban board...');
    
    // Wait for DOM to be fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initializeKanbanComponents, 100);
        });
    } else {
        setTimeout(initializeKanbanComponents, 100);
    }
}

function initializeKanbanComponents() {
    console.log('Initializing Kanban components...');
    
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
    
    // Find task data
    const task = window.tasksData?.find(t => t.id == taskId);
    
    if (!task) {
        console.error('Task not found:', taskId);
        alert('Task data not found. Please refresh the page.');
        return;
    }
    
    console.log('Found task:', task);
    
    // List of all form elements we need to populate
    const formElements = {
        'edit_title': task.title || '',
        'edit_description': task.description || '',
        'edit_priority': task.priority || 'medium',
        'edit_complexity': task.complexity || 'medium',
        'edit_team_id': task.team_id || '',
        'edit_estimated_hours': task.estimated_hours || '',
        'edit_assignee_id': task.assignee_id || '',
        'edit_supervisor_id': task.supervisor_id || '',
        'edit_started_at': task.started_at ? task.started_at.split('T')[0] : '',
        'edit_due_date': task.due_date ? task.due_date.split('T')[0] : '',
        'edit_completed_at': task.completed_at ? task.completed_at.split('T')[0] : ''
    };
    
    // Safely populate each field
    for (const [elementId, value] of Object.entries(formElements)) {
        try {
            const element = document.getElementById(elementId);
            if (element) {
                element.value = value;
                console.log(`Set ${elementId} = ${value}`);
            } else {
                console.warn(`Element ${elementId} not found in DOM`);
            }
        } catch (error) {
            console.error(`Error setting ${elementId}:`, error);
        }
    }
    
    // Handle autocomplete fields
    const assigneeInput = document.getElementById('edit_assignee_input');
    if (assigneeInput) {
        if (task.assignee_id && window.teamUsers) {
            const assignee = window.teamUsers.find(u => u.id == task.assignee_id);
            assigneeInput.value = assignee ? (assignee.display_name || assignee.username) : '';
        } else {
            assigneeInput.value = '';
        }
    }
    
    const supervisorInput = document.getElementById('edit_supervisor_input');
    if (supervisorInput) {
        if (task.supervisor_id && window.teamUsers) {
            const supervisor = window.teamUsers.find(u => u.id == task.supervisor_id);
            supervisorInput.value = supervisor ? (supervisor.display_name || supervisor.username) : '';
        } else {
            supervisorInput.value = '';
        }
    }
    
    // Set current task for file uploads
    currentTaskId = taskId;
    
    // Load file attachments
    loadAttachments(taskId);
    
    // Set form action
    const form = document.getElementById('editTaskForm');
    if (form) {
        form.action = `/update_task/${taskId}`;
    }
    
    // Show modal
    try {
        const modalElement = document.getElementById('editTaskModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
            console.log('Modal shown successfully');
        } else {
            console.error('Edit modal element not found');
        }
    } catch (error) {
        console.error('Error showing modal:', error);
    }
}

// Export immediately after definition
window.loadTaskForEdit = loadTaskForEdit;

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
    const todoCount = document.querySelectorAll('#todo-column .task-card:not([style*="display: none"])').length;
    const inProgressCount = document.querySelectorAll('#in-progress-column .task-card:not([style*="display: none"])').length;
    const inReviewCount = document.querySelectorAll('#in-review-column .task-card:not([style*="display: none"])').length;
    const completedCount = document.querySelectorAll('#completed-column .task-card:not([style*="display: none"])').length;
    
    // Update badges
    const todoBadge = document.querySelector('.kanban-column:nth-child(1) .badge');
    const inProgressBadge = document.querySelector('.kanban-column:nth-child(2) .badge');
    const inReviewBadge = document.querySelector('.kanban-column:nth-child(3) .badge');
    const completedBadge = document.querySelector('.kanban-column:nth-child(4) .badge');
    
    if (todoBadge) todoBadge.textContent = todoCount;
    if (inProgressBadge) inProgressBadge.textContent = inProgressCount;
    if (inReviewBadge) inReviewBadge.textContent = inReviewCount;
    if (completedBadge) completedBadge.textContent = completedCount;
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
    
    // Auto-dismiss after 4 seconds
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 150);
        }
    }, 4000);
    
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
    const currentUserRole = window.currentUserRole; // Role information from template
    
    taskCards.forEach(card => {
        if (filterValue === 'my-tasks') {
            const assigneeId = card.dataset.assigneeId;
            const createdBy = card.dataset.createdBy;
            const supervisorId = card.dataset.supervisorId;
            const taskStatus = card.closest('.task-container').id; // Get column ID to determine status
            
            console.log(`Task ${card.dataset.taskId}: assignee=${assigneeId}, supervisor=${supervisorId}, status=${taskStatus}, currentUser=${currentUserId}, role=${currentUserRole}`);
            
            let showTask = false;
            
            // Always show tasks assigned to current user
            if (assigneeId && assigneeId === currentUserId) {
                showTask = true;
            }
            
            // For administrators: also show unassigned tasks they created
            if (currentUserRole === 'administrator' && !assigneeId && createdBy === currentUserId) {
                showTask = true;
            }
            
            // For regular users: also show tasks they created
            if (currentUserRole !== 'administrator' && createdBy === currentUserId) {
                showTask = true;
            }
            
            // For managers/directors: also show In Review tasks where they are supervisor
            if ((currentUserRole === 'manager' || currentUserRole === 'director') && 
                taskStatus === 'in-review-column' && 
                supervisorId && supervisorId === currentUserId) {
                console.log(`Supervisor match found - Task: ${card.dataset.taskId}, Supervisor: ${supervisorId}, Current User: ${currentUserId}`);
                showTask = true;
            }
            
            card.style.display = showTask ? '' : 'none';
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

function initializeAutocomplete() {
    // Get team users data from backend
    fetchTeamUsers().then(users => {
        console.log('Team users loaded:', users);
        // Initialize autocomplete for create task modal
        setupAutocomplete('assignee_input', 'assignee_id', 'assignee_dropdown', users, 'all');
        setupAutocomplete('supervisor_input', 'supervisor_id', 'supervisor_dropdown', users, 'manager');
        
        // Initialize autocomplete for edit task modal
        setupAutocomplete('edit_assignee_input', 'edit_assignee_id', 'edit_assignee_dropdown', users, 'all');
        setupAutocomplete('edit_supervisor_input', 'edit_supervisor_id', 'edit_supervisor_dropdown', users, 'manager');
        
        // Store users data globally for the edit function
        window.teamUsers = users;
    }).catch(error => {
        console.error('Failed to initialize autocomplete:', error);
    });
}

async function fetchTeamUsers() {
    try {
        const response = await fetch('/api/team-users');
        if (!response.ok) {
            throw new Error('Failed to fetch team users');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching team users:', error);
        return [];
    }
}

function setupAutocomplete(inputId, hiddenId, dropdownId, users, roleFilter) {
    const input = document.getElementById(inputId);
    const hiddenInput = document.getElementById(hiddenId);
    const dropdown = document.getElementById(dropdownId);
    
    if (!input || !hiddenInput || !dropdown) return;
    
    // Filter users based on role
    let filteredUsers = users;
    if (roleFilter === 'manager') {
        filteredUsers = users.filter(user => user.role === 'manager');
    }
    
    input.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        
        if (query.length === 0) {
            dropdown.style.display = 'none';
            hiddenInput.value = '';
            return;
        }
        
        // Filter users based on query
        const matches = filteredUsers.filter(user => {
            const displayName = user.display_name || '';
            const username = user.username || '';
            return displayName.toLowerCase().includes(query) || 
                   username.toLowerCase().includes(query);
        });
        
        if (matches.length === 0) {
            dropdown.style.display = 'none';
            return;
        }
        
        // Build dropdown HTML
        dropdown.innerHTML = matches.map(user => `
            <button type="button" class="dropdown-item" data-user-id="${user.id}" data-user-name="${user.display_name || user.username}">
                ${user.display_name || user.username} (${user.username})
            </button>
        `).join('');
        
        // Add click handlers
        dropdown.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', function() {
                const userId = this.getAttribute('data-user-id');
                const userName = this.getAttribute('data-user-name');
                
                input.value = userName;
                hiddenInput.value = userId;
                dropdown.style.display = 'none';
            });
        });
        
        dropdown.style.display = 'block';
    });
    
    // Hide dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
    
    // Handle keyboard navigation
    input.addEventListener('keydown', function(e) {
        const items = dropdown.querySelectorAll('.dropdown-item');
        let activeItem = dropdown.querySelector('.dropdown-item.active');
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (!activeItem) {
                items[0]?.classList.add('active');
            } else {
                activeItem.classList.remove('active');
                const nextItem = activeItem.nextElementSibling || items[0];
                nextItem.classList.add('active');
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (!activeItem) {
                items[items.length - 1]?.classList.add('active');
            } else {
                activeItem.classList.remove('active');
                const prevItem = activeItem.previousElementSibling || items[items.length - 1];
                prevItem.classList.add('active');
            }
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (activeItem) {
                activeItem.click();
            }
        } else if (e.key === 'Escape') {
            dropdown.style.display = 'none';
        }
    });
}

// File Attachment Management
let currentTaskId = null;

function initializeFileUpload() {
    const fileInput = document.getElementById('fileUpload');
    const uploadArea = document.querySelector('.upload-area');
    
    if (!fileInput || !uploadArea) return;
    
    // File input change handler
    fileInput.addEventListener('change', function(e) {
        const files = Array.from(e.target.files);
        if (files.length > 0) {
            uploadFiles(files);
        }
    });
    
    // Drag and drop handlers
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.borderColor = '#0052CC';
        this.style.backgroundColor = '#f8f9ff';
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.style.borderColor = '#e1e5e9';
        this.style.backgroundColor = 'transparent';
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.borderColor = '#e1e5e9';
        this.style.backgroundColor = 'transparent';
        
        const files = Array.from(e.dataTransfer.files);
        if (files.length > 0) {
            uploadFiles(files);
        }
    });
}

function uploadFiles(files) {
    if (!currentTaskId) {
        showNotification('No task selected for file upload', 'error');
        return;
    }
    
    const progressContainer = document.getElementById('uploadProgress');
    const progressBar = progressContainer.querySelector('.progress-bar');
    
    progressContainer.classList.remove('d-none');
    
    // Upload files one by one
    let uploaded = 0;
    const total = files.length;
    
    files.forEach((file, index) => {
        const formData = new FormData();
        formData.append('file', file);
        
        fetch(`/upload_file/${currentTaskId}`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            uploaded++;
            const progress = (uploaded / total) * 100;
            progressBar.style.width = progress + '%';
            
            if (data.success) {
                showNotification(data.message, 'success');
                loadAttachments(currentTaskId);
            } else {
                showNotification(data.error || 'Upload failed', 'error');
            }
            
            if (uploaded === total) {
                setTimeout(() => {
                    progressContainer.classList.add('d-none');
                    progressBar.style.width = '0%';
                }, 1000);
            }
        })
        .catch(error => {
            uploaded++;
            showNotification('Upload failed: ' + error.message, 'error');
            
            if (uploaded === total) {
                setTimeout(() => {
                    progressContainer.classList.add('d-none');
                    progressBar.style.width = '0%';
                }, 1000);
            }
        });
    });
}

function loadAttachments(taskId) {
    if (!taskId) return;
    
    fetch(`/api/task/${taskId}/attachments`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayAttachments(data.attachments);
            }
        })
        .catch(error => {
            console.error('Failed to load attachments:', error);
        });
}

function displayAttachments(attachments) {
    const container = document.getElementById('attachmentsList');
    if (!container) return;
    
    if (!attachments || attachments.length === 0) {
        container.innerHTML = '<div class="text-muted text-center py-2">No files attached</div>';
        return;
    }
    
    container.innerHTML = attachments.map(attachment => `
        <div class="attachment-item d-flex align-items-center justify-content-between p-2 border rounded mb-2">
            <div class="d-flex align-items-center">
                <i data-feather="file" class="text-muted me-2" style="width: 16px; height: 16px;"></i>
                <div>
                    <div class="fw-medium">${attachment.original_filename}</div>
                    <small class="text-muted">${formatFileSize(attachment.file_size)} • ${new Date(attachment.uploaded_at).toLocaleDateString()}</small>
                </div>
            </div>
            <div class="d-flex align-items-center">
                <a href="/download_file/${attachment.id}" class="btn btn-sm btn-outline-primary me-2" title="Download">
                    <i data-feather="download" style="width: 12px; height: 12px;"></i>
                </a>
                <button type="button" class="btn btn-sm btn-outline-danger" onclick="deleteAttachment('${attachment.id}')" title="Delete">
                    <i data-feather="trash-2" style="width: 12px; height: 12px;"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    // Refresh icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function deleteAttachment(attachmentId) {
    if (!confirm('Are you sure you want to delete this file?')) {
        return;
    }
    
    fetch(`/delete_file/${attachmentId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            loadAttachments(currentTaskId);
        } else {
            showNotification(data.error || 'Delete failed', 'error');
        }
    })
    .catch(error => {
        showNotification('Delete failed: ' + error.message, 'error');
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Priority Management Functions
function cyclePriority(event, taskId, currentPriority) {
    // Stop event from bubbling to prevent opening edit modal
    event.stopPropagation();
    event.preventDefault();
    
    // Define priority cycle
    const priorityCycle = ['low', 'medium', 'high', 'urgent'];
    const currentIndex = priorityCycle.indexOf(currentPriority);
    const nextIndex = (currentIndex + 1) % priorityCycle.length;
    const newPriority = priorityCycle[nextIndex];
    
    console.log(`Cycling priority for task ${taskId}: ${currentPriority} -> ${newPriority}`);
    
    updateTaskPriority(taskId, newPriority);
}

function updateTaskPriority(taskId, newPriority) {
    const button = document.querySelector(`[data-task-id="${taskId}"].priority-btn`);
    
    if (!button) {
        console.error('Priority button not found for task:', taskId);
        return;
    }
    
    // Show loading state
    button.disabled = true;
    button.classList.add('priority-loading');
    
    const formData = new FormData();
    formData.append('priority', newPriority);
    
    fetch(`/update_task_priority/${taskId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updatePriorityUI(taskId, newPriority);
            showNotification(`Priority updated to ${newPriority}`, 'success');
            
            // Update tasks data if available
            if (window.tasksData) {
                const task = window.tasksData.find(t => t.id == taskId);
                if (task) {
                    task.priority = newPriority;
                }
            }
        } else {
            showNotification(data.error || 'Failed to update priority', 'error');
        }
    })
    .catch(error => {
        console.error('Error updating priority:', error);
        showNotification('Failed to update priority', 'error');
    })
    .finally(() => {
        button.disabled = false;
        button.classList.remove('priority-loading');
    });
}

function updatePriorityUI(taskId, newPriority) {
    const button = document.querySelector(`[data-task-id="${taskId}"].priority-btn`);
    const taskCard = document.querySelector(`[data-task-id="${taskId}"].task-card`);
    
    if (!button || !taskCard) return;
    
    // Update button classes
    button.className = `btn btn-sm priority-btn priority-${newPriority}`;
    button.setAttribute('data-current-priority', newPriority);
    
    // Update task card class
    taskCard.className = taskCard.className.replace(/priority-\w+/, `priority-${newPriority}`);
    
    // Update icon
    const icon = button.querySelector('i');
    const iconMap = {
        'urgent': 'alert-triangle',
        'high': 'arrow-up',
        'medium': 'minus',
        'low': 'arrow-down'
    };
    
    if (icon) {
        icon.setAttribute('data-feather', iconMap[newPriority]);
    }
    
    // Update text
    const textSpan = button.querySelector('.priority-text');
    if (textSpan) {
        textSpan.textContent = newPriority.charAt(0).toUpperCase() + newPriority.slice(1);
    }
    
    // Add animation effect
    button.classList.add('priority-updated');
    setTimeout(() => {
        button.classList.remove('priority-updated');
    }, 500);
    
    // Refresh feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

// Export functions for global use
window.loadTaskForEdit = loadTaskForEdit;
window.updateTaskStatus = updateTaskStatus;
window.showNotification = showNotification;
window.refreshIcons = refreshIcons;
window.toggleTimeTracking = toggleTimeTracking;
window.updateTaskEstimate = updateTaskEstimate;
window.deleteAttachment = deleteAttachment;
window.initializeFileUpload = initializeFileUpload;
window.cyclePriority = cyclePriority;
