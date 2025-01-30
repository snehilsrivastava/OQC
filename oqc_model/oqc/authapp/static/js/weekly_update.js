const modelLinks = document.querySelectorAll('a[onclick^="toggleTable("]');
modelLinks.forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();

        const chevronIcon = this.querySelector('span');

        if (chevronIcon.style.transform === 'rotate(90deg) translateX(10%) translateY(0%)') {
            chevronIcon.style.transform = 'rotate(0deg)';
        } else {
            chevronIcon.style.transform = 'rotate(90deg) translateX(10%) translateY(0%)';
        }
    });
});

function togglePopup() {
    var popup = document.getElementById("popup");
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

$(document).ready(function () {
    $('#searchInput').on('keyup', function () {
        var searchTerm = $(this).val().toLowerCase();

        // Filter list items (models)
        $('#models-container ul li').each(function () {
            var modelName = $(this).find('a').text().toLowerCase();
            if (modelName.indexOf(searchTerm) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});

function showModels(productName) {
    const allModelTables = document.querySelectorAll('.model-table');
    allModelTables.forEach(table => table.style.display = 'none');

    const selectedProductModels = document.getElementById('models-' + productName);
    selectedProductModels.style.display = 'block';

    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    const activeTab = Array.from(tabs).find(tab => tab.textContent.trim() === productName);
    if (activeTab) activeTab.classList.add('active');
}

function toggleTable(modelId) {
    const table = document.getElementById('model-table-' + modelId);
    table.style.display = table.style.display === 'none' ? 'block' : 'none';
}

// Default behavior: show the first product's models by default
document.addEventListener('DOMContentLoaded', () => {
    const firstProduct = document.querySelector('.tab');
    if (firstProduct) {
        firstProduct.click();
    }
});

function initializeDataTable(products) {
    $(document).ready(function () {
        $('table').DataTable({
            paging: false,
            searching: false,
            ordering: false,
            info: false,
        });
    
        $('table').on('click', 'td.editable', function (event) {
            const $table = $(this).closest('table');
            const tableClasses = $table.attr('class').split(' ');
            if (tableClasses.some(className => products.includes(className))) {
                $(this).addClass('selected');
                $(this).siblings().removeClass('selected');
                $(this).parent().siblings().find('td').removeClass('selected');
            }
        });
    
        $('table').on('dblclick', 'td.editable', function () {
            const $table = $(this).closest('table');
            const tableClasses = $table.attr('class').split(' ');
            if (tableClasses.some(className => products.includes(className))) {
                const $cell = $(this);
                const originalValue = $cell.html().replace(/<br\s*\/?>/g, '\n');
                const $textarea = $('<textarea>' + originalValue + '</textarea>');
                $cell.empty().append($textarea);
                $textarea.focus();
                $textarea[0].setSelectionRange($textarea.val().length, $textarea.val().length);
                const scrollHeight = $textarea[0].scrollHeight;
                $textarea.height(scrollHeight);
                const $row = $textarea.closest('tr');
                $row.height(scrollHeight);
    
                $textarea.on('input', function () {
                    const scrollHeight = $textarea[0].scrollHeight;
                    $textarea.height(scrollHeight);
                });
    
                $textarea.on('blur', function () {
                    const newValue = $(this).val();
                    $cell.html(newValue.replace(/\n/g, '<br>').replace(/ /g, '&nbsp;'));
    
                    if (newValue !== originalValue) {
                        const row = $cell.closest('tr');
                        const firstCellText = row.find('td:first-child').text();
                        const headerText = $cell.closest('table').find('th').eq($cell.index()).text();
                        const product = $('div.tab.active').text();
                        const model = $cell.closest('li').find('a').text().trim();
                        $.ajax({
                            url: '/update_cell/',
                            type: 'POST',
                            data: {
                                row: firstCellText,
                                col: headerText,
                                value: newValue,
                                product: product,
                                model: model,
                            }
                        });
                    }
                });
            }
        });
    });
}