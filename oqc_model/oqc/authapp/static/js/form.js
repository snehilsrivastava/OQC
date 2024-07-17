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

