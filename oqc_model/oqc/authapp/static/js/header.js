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
    var clickedElement = event.target;
    if (clickedElement !== document.getElementById("userInfo") && clickedElement !== document.getElementById("userButton") && clickedElement !== document.getElementById("userButtonIcon")) {
        document.getElementById("userInfo").style.display = "none";
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
            alert('Logout failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Logout failed');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Check local storage
    let localS = localStorage.getItem('theme'),
        themeToSet = localS;

    // If local storage is not set, we check the OS preference
    console.log(localS);
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

    // Update the icon visibility based on the current theme
    const updateIcons = (theme) => {
        document.getElementById('theme-switcher__sun').style.display = (theme === 'light') ? 'block' : 'none';
        document.getElementById('theme-switcher__moon').style.display = (theme === 'dark') ? 'block' : 'none';
    };

    updateIcons(themeToSet);

    // Theme switcher function
    const switchTheme = () => {
        const rootElem = document.documentElement;
        let dataTheme = rootElem.getAttribute('data-theme');
        let newTheme = (dataTheme === 'light') ? 'dark' : 'light';

        rootElem.setAttribute('data-theme', newTheme);
        localStorage.setItem("theme", newTheme);
        updateIcons(newTheme);
    };

    // Add the event listener for the theme switcher
    document.querySelector('#theme-switcher').addEventListener('click', switchTheme);
});