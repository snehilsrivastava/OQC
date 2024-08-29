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

function filterOnStage(button, stage) {
    const parentRow = button.closest('tr');
    const collapseRow = parentRow.nextElementSibling;
    const collapseTable = collapseRow.querySelector('.drop-table');
    const collapseBody = collapseTable.querySelector('tbody');
    const rows = collapseBody.querySelectorAll('tr');
    const isFiltered = button.getAttribute('data-filtered') === 'true';

    if (isFiltered) {
        // Clear the filter and reset the button state
        rows.forEach(row => {
            row.style.display = '';
        });
        button.setAttribute('data-filtered', false);
        button.classList.remove('stage-filter-btn-active');
    } else {
        // Remove the active state from all buttons in the same row
        const buttons = button.closest('td').querySelectorAll('button');
        buttons.forEach(btn => {
            btn.classList.remove('stage-filter-btn-active');
            btn.setAttribute('data-filtered', false); // Reset all other buttons' state
        });

        // Apply the new filter
        rows.forEach(row => {
            const stageValue = row.cells[2].textContent.trim();
            row.style.display = stageValue === stage ? '' : 'none';
        });

        // Set the active state for the clicked button
        button.setAttribute('data-filtered', true);
        button.classList.add('stage-filter-btn-active');
    }
}
