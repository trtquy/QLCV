// Team Management JavaScript

function initializeTeam() {
    console.log('Initializing team management...');
    
    // Initialize role management
    initializeRoleManagement();
    
    // Initialize team statistics
    initializeTeamStats();
    
    // Initialize member interactions
    initializeMemberInteractions();
    
    // Initialize feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function initializeRoleManagement() {
    // Role update form handling
    const roleForm = document.getElementById('roleForm');
    if (roleForm) {
        roleForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Updating...';
            
            // Submit the form
            fetch(this.action, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    // Close modal and reload page
                    const modal = bootstrap.Modal.getInstance(document.getElementById('roleModal'));
                    modal.hide();
                    
                    showNotification('User role updated successfully!', 'success');
                    
                    // Reload page after a short delay
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    throw new Error('Failed to update role');
                }
            })
            .catch(error => {
                console.error('Error updating role:', error);
                showNotification('Failed to update user role', 'error');
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            });
        });
    }
}

function initializeTeamStats() {
    // Animate progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-in-out';
            bar.style.width = targetWidth;
        }, 100);
    });
    
    // Animate stat numbers
    animateStatNumbers();
}

function animateStatNumbers() {
    const statValues = document.querySelectorAll('.stats-value, .h4');
    
    statValues.forEach(element => {
        const finalValue = parseInt(element.textContent) || 0;
        if (finalValue > 0 && finalValue < 100) { // Only animate reasonable numbers
            let currentValue = 0;
            const increment = Math.ceil(finalValue / 20);
            
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= finalValue) {
                    currentValue = finalValue;
                    clearInterval(timer);
                }
                element.textContent = currentValue;
            }, 50);
        }
    });
}

function initializeMemberInteractions() {
    // Member card hover effects
    const memberCards = document.querySelectorAll('.team-member-card');
    
    memberCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Quick actions
    initializeQuickActions();
    
    // Member filtering
    initializeMemberFiltering();
}

function initializeQuickActions() {
    // Add quick action buttons (if manager)
    const badges = document.querySelectorAll('.badge');
    let isManager = false;
    
    badges.forEach(badge => {
        if (badge.textContent.includes("Manager Access")) {
            isManager = true;
        }
    });
    
    if (isManager) {
        addManagerQuickActions();
    }
}

function addManagerQuickActions() {
    // Add bulk role update functionality
    const headerActions = document.querySelector('.row.mb-4 .col');
    if (headerActions) {
        const actionsContainer = document.createElement('div');
        actionsContainer.className = 'mt-2';
        actionsContainer.innerHTML = `
            <div class="btn-group" role="group">
                <button type="button" class="btn btn-outline-primary btn-sm" onclick="toggleMemberSelection()">
                    <i data-feather="check-square" class="me-1"></i>
                    Select Members
                </button>
                <button type="button" class="btn btn-outline-secondary btn-sm" onclick="exportTeamData()">
                    <i data-feather="download" class="me-1"></i>
                    Export Data
                </button>
            </div>
        `;
        
        headerActions.appendChild(actionsContainer);
        
        // Refresh icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
}

function toggleMemberSelection() {
    const memberCards = document.querySelectorAll('.team-member-card');
    const isSelectionMode = document.querySelector('.member-checkbox');
    
    if (!isSelectionMode) {
        // Add checkboxes
        memberCards.forEach(card => {
            const checkbox = document.createElement('div');
            checkbox.className = 'member-checkbox position-absolute';
            checkbox.style.cssText = 'top: 45px; left: 15px; z-index: 10;';
            checkbox.innerHTML = `
                <input type="checkbox" class="form-check-input" value="${card.dataset.userId}">
            `;
            card.appendChild(checkbox);
            card.style.cursor = 'pointer';
        });
        
        // Add bulk actions
        showBulkActions();
    } else {
        // Remove checkboxes
        document.querySelectorAll('.member-checkbox').forEach(checkbox => {
            checkbox.remove();
        });
        hideBulkActions();
        
        memberCards.forEach(card => {
            card.style.cursor = '';
        });
    }
}

function showBulkActions() {
    const bulkActions = document.createElement('div');
    bulkActions.id = 'bulkActions';
    bulkActions.className = 'position-fixed bg-white shadow-lg rounded p-3';
    bulkActions.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border: 1px solid #dee2e6;';
    bulkActions.innerHTML = `
        <div class="d-flex align-items-center gap-2">
            <span class="text-muted small">Selected: <span id="selectedCount">0</span></span>
            <button class="btn btn-primary btn-sm" onclick="bulkUpdateRole('manager')">Make Managers</button>
            <button class="btn btn-outline-primary btn-sm" onclick="bulkUpdateRole('member')">Make Members</button>
            <button class="btn btn-outline-secondary btn-sm" onclick="toggleMemberSelection()">Cancel</button>
        </div>
    `;
    
    document.body.appendChild(bulkActions);
    
    // Update selected count
    document.addEventListener('change', function(e) {
        if (e.target.matches('.member-checkbox input')) {
            updateSelectedCount();
        }
    });
}

function hideBulkActions() {
    const bulkActions = document.getElementById('bulkActions');
    if (bulkActions) {
        bulkActions.remove();
    }
}

function updateSelectedCount() {
    const selectedCheckboxes = document.querySelectorAll('.member-checkbox input:checked');
    const countElement = document.getElementById('selectedCount');
    if (countElement) {
        countElement.textContent = selectedCheckboxes.length;
    }
}

function bulkUpdateRole(newRole) {
    const selectedCheckboxes = document.querySelectorAll('.member-checkbox input:checked');
    const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
    
    if (selectedIds.length === 0) {
        showNotification('Please select at least one member', 'warning');
        return;
    }
    
    if (confirm(`Are you sure you want to update ${selectedIds.length} member(s) to ${newRole}?`)) {
        // In a real application, this would be a batch API call
        selectedIds.forEach(userId => {
            // Simulate API call
            console.log(`Updating user ${userId} to role ${newRole}`);
        });
        
        showNotification(`Updated ${selectedIds.length} member(s) successfully!`, 'success');
        toggleMemberSelection(); // Exit selection mode
        
        // Reload page to show changes
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }
}

function initializeMemberFiltering() {
    // Add filter controls
    const cardHeader = document.querySelector('.card-header');
    if (cardHeader) {
        const filterContainer = document.createElement('div');
        filterContainer.className = 'mt-2';
        filterContainer.innerHTML = `
            <div class="row align-items-center">
                <div class="col-md-6">
                    <input type="text" class="form-control form-control-sm" 
                           id="memberSearch" placeholder="Search members...">
                </div>
                <div class="col-md-3">
                    <select class="form-select form-select-sm" id="roleFilter">
                        <option value="">All Roles</option>
                        <option value="manager">Managers</option>
                        <option value="member">Members</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select class="form-select form-select-sm" id="sortBy">
                        <option value="name">Sort by Name</option>
                        <option value="role">Sort by Role</option>
                        <option value="tasks">Sort by Tasks</option>
                        <option value="completion">Sort by Completion</option>
                    </select>
                </div>
            </div>
        `;
        
        cardHeader.appendChild(filterContainer);
        
        // Add event listeners
        document.getElementById('memberSearch').addEventListener('input', filterMembers);
        document.getElementById('roleFilter').addEventListener('change', filterMembers);
        document.getElementById('sortBy').addEventListener('change', sortMembers);
    }
}

function filterMembers() {
    const searchTerm = document.getElementById('memberSearch').value.toLowerCase();
    const roleFilter = document.getElementById('roleFilter').value;
    const memberCards = document.querySelectorAll('.team-member-card');
    
    memberCards.forEach(card => {
        const memberName = card.querySelector('h5').textContent.toLowerCase();
        const memberRole = card.querySelector('.role-badge .badge').textContent.toLowerCase();
        
        const matchesSearch = !searchTerm || memberName.includes(searchTerm);
        const matchesRole = !roleFilter || memberRole.includes(roleFilter);
        
        if (matchesSearch && matchesRole) {
            card.closest('.col-lg-6').style.display = '';
        } else {
            card.closest('.col-lg-6').style.display = 'none';
        }
    });
}

function sortMembers() {
    const sortBy = document.getElementById('sortBy').value;
    const container = document.querySelector('.row.g-4');
    const memberColumns = Array.from(container.querySelectorAll('.col-lg-6'));
    
    memberColumns.sort((a, b) => {
        const cardA = a.querySelector('.team-member-card');
        const cardB = b.querySelector('.team-member-card');
        
        switch (sortBy) {
            case 'name':
                const nameA = cardA.querySelector('h5').textContent;
                const nameB = cardB.querySelector('h5').textContent;
                return nameA.localeCompare(nameB);
            
            case 'role':
                const roleA = cardA.querySelector('.role-badge .badge').textContent;
                const roleB = cardB.querySelector('.role-badge .badge').textContent;
                return roleA.localeCompare(roleB);
            
            case 'tasks':
                const tasksA = parseInt(cardA.querySelector('.stats-value').textContent) || 0;
                const tasksB = parseInt(cardB.querySelector('.stats-value').textContent) || 0;
                return tasksB - tasksA; // Descending
            
            case 'completion':
                const progressA = parseFloat(cardA.querySelector('.progress-bar').style.width) || 0;
                const progressB = parseFloat(cardB.querySelector('.progress-bar').style.width) || 0;
                return progressB - progressA; // Descending
            
            default:
                return 0;
        }
    });
    
    // Re-append sorted elements
    memberColumns.forEach(column => {
        container.appendChild(column);
    });
}

function exportTeamData() {
    // Collect team data for export
    const teamData = {
        exportDate: new Date().toISOString(),
        members: [],
        summary: {
            totalMembers: 0,
            managers: 0,
            members: 0,
            totalTasks: 0
        }
    };
    
    // Extract member data from DOM
    const memberCards = document.querySelectorAll('.team-member-card');
    memberCards.forEach(card => {
        const name = card.querySelector('h5').textContent;
        const role = card.querySelector('.role-badge .badge').textContent.toLowerCase();
        const statsValues = card.querySelectorAll('.stats-value');
        
        teamData.members.push({
            name: name,
            role: role,
            totalTasks: parseInt(statsValues[0]?.textContent) || 0,
            completedTasks: parseInt(statsValues[1]?.textContent) || 0,
            activeTasks: parseInt(statsValues[2]?.textContent) || 0
        });
        
        teamData.summary.totalMembers++;
        if (role === 'manager') {
            teamData.summary.managers++;
        } else {
            teamData.summary.members++;
        }
        teamData.summary.totalTasks += parseInt(statsValues[0]?.textContent) || 0;
    });
    
    // Create and download file
    const dataStr = JSON.stringify(teamData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `team-data-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    
    showNotification('Team data exported successfully!', 'success');
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

// Member profile modal (future enhancement)
function showMemberProfile(userId) {
    // This would show detailed member information
    console.log('Showing profile for user:', userId);
}

// Initialize team management when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeTeam();
});

// Export functions for global use
window.initializeTeam = initializeTeam;
window.exportTeamData = exportTeamData;
window.showMemberProfile = showMemberProfile;
window.toggleMemberSelection = toggleMemberSelection;
window.bulkUpdateRole = bulkUpdateRole;
