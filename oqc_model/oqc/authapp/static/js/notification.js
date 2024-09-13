function markAllAsRead() {
    fetch('/mark_all_as_read/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({}),
    }).then(response => {
        window.location.reload();
    });
}

function deleteNotification(action, metadata, created_at) {
    fetch('/delete_notification/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: action, metadata: metadata, created_at: created_at }),
    }).then(response => {
        window.location.reload();
    });
}