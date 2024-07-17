  function toggleMenu() {
        var sidebar = document.getElementById("sidebar");
        if (sidebar.style.display === "block") {
            sidebar.style.display = "none";
        } else {
            sidebar.style.display = "block";
        }
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
    
    

    // Ensure user info starts hidden
    document.addEventListener("DOMContentLoaded", function() {
        var sidebar = document.getElementById("userInfo");
        sidebar.style.display = "none";
    });
    

    $(document).ready(function () {
        $('.collapse').on('show.bs.collapse', function () {
            var target = $(this).prev().find('button i.fas');
            target.removeClass('fa-chevron-down').addClass('fa-chevron-up');
        }).on('hide.bs.collapse', function () {
            var target = $(this).prev().find('button i.fas');
            target.removeClass('fa-chevron-up').addClass('fa-chevron-down');
        });
    });

    function toggleCollapseIcon(button) {
        var icon = button.querySelector('i.fas');
        icon.classList.toggle('fa-chevron-down');
        icon.classList.toggle('fa-chevron-up');
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Select all checkboxes when the "select-all" checkbox is clicked
        document.querySelectorAll('[id^="select-all-"]').forEach(checkbox => {
            checkbox.addEventListener('click', function(event) {
                const table = event.target.closest('table'); // Find the closest table
                const checkboxes = table.querySelectorAll('td input[type="checkbox"]'); // Get all checkboxes within the table
                for (const checkbox of checkboxes) {
                    checkbox.checked = event.target.checked;
                }
            });
        });
    });
    
    document.addEventListener('click', function(event) {
    var clickedElement = event.target;
    if (clickedElement !== document.getElementById("userInfo") && clickedElement !== document.getElementById("userButton") && clickedElement !== document.getElementById("userButtonIcon")) {
        document.getElementById("userInfo").style.display = "none";
    }
    });

    
        