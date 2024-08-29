function toggleMenu() {
    var sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("visible");
}

function toggleFilter() {
    var popup = document.getElementById("filterPopup");
    var overlay = document.getElementById("overlay");
    var display = popup.style.display;

    if (display === "block") {
        popup.style.display = "none";
        overlay.style.display = "none";
    } else {
        popup.style.display = "block";
        overlay.style.display = "block";
    }
}

function toggleUserInfo() {
    var sidebar = document.getElementById("userInfo");
    if (sidebar.style.display === "block" || sidebar.style.display === "") {
        sidebar.style.display = "none";
    } else {
        sidebar.style.display = "block";
    }
}

function clearFilter() {
    var form = document.getElementById("filter-form");
    // Manually reset each field to the empty string or their default values if needed
    var product = document.getElementById("product");
    var testStage = document.getElementById("test_stage");
    var modelName = document.getElementById("model_name");
    var testName = document.getElementById("test_name");
    var serialNumber = document.getElementById("serial_number");
    var B_status = document.getElementById("B_status");
    var status = document.getElementById("status");
    var L_status = document.getElementById("L_status");
    var startDate = document.getElementById("start_date");
    var endDate = document.getElementById("end_date");

    // Set default values
    product.value = "";
    testStage.value = "";
    modelName.value = "";
    testName.value = "";
    serialNumber.value = "";
    B_status.value = "";
    L_status.value = "";
    status.value = "";
    startDate.value = "";
    endDate.value = "";
}

function toggleCollapseIcon(button) {
    var icon = button.querySelector('i.fas');
    icon.classList.toggle('fa-chevron-down');
    icon.classList.toggle('fa-chevron-up');
}


function toggleAllCollapseButtons() {
    var masterButton = document.querySelector('.master-collapse-button');
    var masterIcon = masterButton.querySelector('i.fas');
    var isExpanded = masterIcon.classList.contains('fa-chevron-up');
    masterIcon.classList.toggle('fa-chevron-down', isExpanded);
    masterIcon.classList.toggle('fa-chevron-up', !isExpanded);
    var collapseButtons = document.querySelectorAll('.collapse-button:not(.master-collapse-button)');

    collapseButtons.forEach(function(button) {
        var target = button.getAttribute('data-target');
        var collapseContent = document.querySelector(target);
        if (isExpanded) {
            if (collapseContent.classList.contains('show')) {
                button.click();
            }
        } else {
            if (!collapseContent.classList.contains('show')) {
                button.click();
            }
        }
    });
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

    if (sidebar.classList.contains("visible") && !sidebar.contains(event.target) && !header.contains(event.target)) {
        sidebar.classList.remove("visible");
    }
}
document.addEventListener("click", handleOutsideClick);