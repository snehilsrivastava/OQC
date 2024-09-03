function toggleMenu() {
    var sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("visible");
}

document.querySelectorAll('.dropdown-toggle').forEach(item => {
    item.addEventListener('click', function(e) {
        e.preventDefault();
        let target = document.querySelector(this.getAttribute('href'));
        let icon = this.querySelector('.chevron-icon');

        if (target.classList.contains('show')) {
            target.classList.remove('show');
            icon.style.transform = 'rotate(0deg)';
        } else {
            target.classList.add('show');
            icon.style.transform = 'rotate(90deg) translateX(10%) translateY(-5%)';
        }
    });
});

function handleOutsideClick(event) {
    const sidebar = document.getElementById("sidebar");
    const header = document.querySelector(".header");
    if (sidebar) {
        if (sidebar.classList.contains("visible") && !sidebar.contains(event.target) && !header.contains(event.target)) {
            sidebar.classList.remove("visible");
        }
    }
}

document.addEventListener("click", handleOutsideClick);
    
function toggleUserInfo() {
    var sidebar = document.getElementById("userInfo");
    if (sidebar.style.display === "block" || sidebar.style.display === "") {
        sidebar.style.display = "none";
    } else {
        sidebar.style.display = "block";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var sidebar = document.getElementById("userInfo");
    sidebar.style.display = "none";
});

document.addEventListener('click', function(event) {
    var userInfo = document.getElementById("userInfo");
    var userButton = document.getElementById("userButton");
    
    if (!userInfo.contains(event.target) && !userButton.contains(event.target)) {
        userInfo.style.display = "none";
    }
});

function logoutUser() {
    fetch('/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Redirect to the home page or show a success message
            window.location.href = '/';
        } else {
            window.location.href = '/';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.href = '/';
    });
}

function toggleNotifications() {
    const notifInfo = document.getElementById("notifInfo");
    notifInfo.classList.toggle("active");
}

document.addEventListener('click', function(event) {
    var notifInfo = document.getElementById("notifInfo");
    var notifButton = document.getElementById("notifButton");
    
    if (!notifInfo.contains(event.target) && !notifButton.contains(event.target)) {
        notifInfo.classList.remove("active");
    }
});

function handleNotification(action, metadata) {
    fetch('/handle_notification/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: action, metadata: metadata })
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        } else {
            console.error('No redirect URL provided in response');
        }
    });
}

function clearNotifications(notifications) {
    const notifClickElements = document.querySelectorAll('.notif-click');
    
    notifClickElements.forEach(element => {
        element.style.transform = 'translate(100%, 0)';
        element.addEventListener('transitionend', () => {
            element.remove();
        });
    });
    fetch('/clear_notification/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({notification: notifications})
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Check local storage
    let localS = localStorage.getItem('theme'),
        themeToSet = localS;

    // If local storage is not set, we check the OS preference
    if (!localS) {
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
        if (prefersDarkScheme.matches) {
            themeToSet = 'dark';
        } else {
            themeToSet = 'light';
        }
    }

    if (themeToSet=="auto") {
        themeToSet = 'dark';
    }
    
    // Set the correct theme
    document.documentElement.setAttribute('data-theme', themeToSet);

    const checkbox = document.getElementById("theme-checkbox");
    if (themeToSet=="dark") {
        checkbox.checked = true;
    }

    // Theme switcher function
    const switchTheme = () => {
        const rootElem = document.documentElement;
        let dataTheme = rootElem.getAttribute('data-theme');
        let newTheme = (dataTheme === 'light') ? 'dark' : 'light';

        rootElem.setAttribute('data-theme', newTheme);
        localStorage.setItem("theme", newTheme);
        // updateIcons(newTheme);    
    };

    // Add the event listener for the theme switcher
    checkbox.addEventListener('change', switchTheme);
});