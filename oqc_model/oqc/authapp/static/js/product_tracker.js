const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        if (mutation.attributeName === 'data-theme') {
            theme = document.documentElement.getAttribute('data-theme');
            for (const key in hotInstances) {
                const hot = hotInstances[key];
                if (theme === 'dark') {
                    hot.updateSettings({ themeName: 'ht-theme-main-dark' });
                }
                else {
                    hot.updateSettings({ themeName: 'ht-theme-main' });
                }
                hot.render();
            }
        }
    });
});
observer.observe(document.documentElement, { attributes: true });

function applyParentChildFormatting(hot, hotData) {
    const tableData = hot.getData();
    const taskRows = [];
    const activityRows = [];
    hotData.forEach((rowData) => {
        const rowIndex = tableData.findIndex(row => row[0] === rowData.task);
        taskRows.push(rowIndex);
        if (rowData.__children) {
            rowData.__children.forEach(child => {
                const childIndex = tableData.findIndex(row => row[0] === child.task);
                activityRows.push(childIndex); 
            });
        }
    });
    taskRows.forEach(row => {
        hot.setCellMeta(row, 0, 'className', 'task-cell');
    });
    activityRows.forEach(row => {
        hot.setCellMeta(row, 0, 'className', 'activity-cell');
    });
    for (let i = 0; i < tableData.length; i++) {
        if (!taskRows.includes(i) && !activityRows.includes(i)) {
            hot.setCellMeta(i, 0, 'className', 'sub-activity-cell');
        }
    }
}

function addWeeks(hot) {
    const tableData = hot.getData();
    let startDate = null;
    let endDate = null;
    for (const row of tableData) {
        const dateStr2 = row[2];
        const dateStr3 = row[3];
        const dateStr4 = row[4];
        const dateStr5 = row[5];
        [dateStr2, dateStr4].forEach(dateStr => {
            if (dateStr) {
                const [day, month, year] = dateStr.split('/').map(Number);
                const date = new Date(year, month - 1, day);

                if (startDate === null || date < startDate) {
                    startDate = date;
                }
            }
        });
        [dateStr3, dateStr5].forEach(dateStr => {
            if (dateStr) {
                const [day, month, year] = dateStr.split('/').map(Number);
                const date = new Date(year, month - 1, day);

                if (endDate === null || date > endDate) {
                    endDate = date;
                }
            }
        });
    }
    startDate = startDate || new Date();
    endDate = endDate || new Date();
    const today = new Date();
    if (today > endDate) {
        endDate = today;
    }

    const nestedHeaders = hot.getSettings().nestedHeaders;
    const columns = hot.getSettings().columns;
    let currentWeekNumber = getISOWeekNumber(startDate);
    let currentDate = new Date(getMonday(startDate));
    columns[columns.length - 1].width = 200;
    while (currentDate <= endDate) {
        const newColumns = [];
        for (let i = 0; i < 7; i++) {
            const dayNumber = currentDate.getDate();
            const newColumn = {
                data: `${dayNumber}/${currentDate.getMonth() + 1}/${currentDate.getFullYear()}`,
                width: 24,
                title: String(dayNumber),
                readOnly: true,
            };
            newColumns.push(newColumn);
            currentDate.setDate(currentDate.getDate() + 1);
        }

        const remarksIndex = columns.findIndex(col => col.data === 'Remarks') || columns.length - 1;
        columns.splice(remarksIndex, 0, ...newColumns);

        const topHeaderRow = nestedHeaders[0];
        const lastElementIndex = topHeaderRow.length;
        const weekStart = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - 7).getDate();
        const weekEnd = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - 1).getDate();
        topHeaderRow.splice(lastElementIndex, 0, {
            label: `WEEK ${ currentWeekNumber } (${ weekStart } - ${ weekEnd } ${ currentDate.toLocaleString('default', { month: 'short' }).toUpperCase() })`,
            colspan: 7,
        });

        const bottomHeaderRow = nestedHeaders[1];
        const bottomInsertIndex = bottomHeaderRow.length - (bottomHeaderRow.includes("Remarks") ? 1 : 0);
        for (let i = 6; i >= 0; i--) {
            const dayNumber = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - (7 - i)).getDate();
            bottomHeaderRow.splice(bottomInsertIndex, 0, dayNumber);
        }

        currentWeekNumber++;
        currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() + (8 - currentDate.getDay()) % 7);
    }
    hot.updateSettings({
        nestedHeaders: nestedHeaders,
        columns: columns,
    });
    hot.render();
}

function parseDate(dateStr) {
      if (!dateStr) return null;
      const [day, month, year] = dateStr.split('/').map(Number);
      const date = new Date(year, month - 1, day);
    if (isNaN(date.getTime())) {
        return null;
    }
    return date;
}

function updateStatus(hot, hotData) {
    function traverseData(data) {
        data.forEach(row => {
            const start_exp = parseDate(row.start_exp);
            const end_exp = parseDate(row.end_exp);
            const start_act = parseDate(row.start_act);
            const end_act = parseDate(row.end_act);

            const today = new Date();
            let status = "";
            if (end_act && end_act < end_exp) {
                status = "DONE IN ADVANCE";
            } else if (end_act && end_exp && end_act.getTime() === end_exp.getTime()) {
                status = "DONE";
            } else if (end_exp && end_act > end_exp) {
                status = "DONE WITH DELAY";
            } else if (!start_act && start_exp > today) {
                status = "IN PLAN";
            } else if (!start_act && start_exp && start_exp < today) {
                status = "DELAYED";
            } else if (!end_act && end_exp && end_exp < today) {
                status = "DELAYED";
            } else if (start_act && start_act < start_exp) {
                status = "STARTED EARLY";
            } else if (!end_act && start_act && start_act <= today) {
                status = "IN PROGRESS";
            }
            row.status = status;
            if (row.__children && row.__children.length > 0) {
                traverseData(row.__children);
            }
        });
    }
    traverseData(hotData);
    hot.render();
}

function addGanttClasses(hot) {
    const columns = hot.getSettings().columns;
    const tableData = hot.getData();
    const today = new Date();
    tableData.forEach((row, rowIndex) => {
        const start_exp = parseDate(row[2]);
        const end_exp = parseDate(row[3]);
        const start_act = parseDate(row[4]);
        const end_act = parseDate(row[5]);
        columns.forEach((column, colIndex) => {
            const date = parseDate(column.data);
            if (date) {
                let className = '';
                hot.setCellMeta(rowIndex, colIndex, 'className', '');
                if ((!start_act && today < start_exp && start_exp <= date && date <= end_exp) || (end_act && end_act < date && date <= end_exp)) {
                    className = 'in-plan';
                } else if (end_act && end_exp && end_act.getTime() === end_exp.getTime() && end_act.getTime() === date.getTime()) {
                    className = 'done';
                } else if (end_act && end_exp && end_act.getTime() === date.getTime() && end_act < end_exp) {
                    className = 'done-in-advance';
                } else if (end_act && end_exp && end_act.getTime() === date.getTime() && end_act > end_exp) {
                    className = 'done-with-delay';
                } else if (start_exp && start_exp <= date && (date < start_act || !start_act) && date <= today) {
                    className = 'delayed';
                } else if (end_exp <= date && date < end_act) {
                    className = 'delayed';
                } else if (start_act && start_act <= date && date < start_exp) {
                    className = 'started-early';
                } else if (start_act && start_act <= date && (date < end_act || (!end_act && date <= today ))) {
                    className = 'in-progress';
                }
                if (className) {
                    hot.setCellMeta(rowIndex, colIndex, 'className', className);
                }
            }
        });
        const status = row[1];
        hot.setCellMeta(rowIndex, 1, 'className', status.replace(/ /g, '-').toLowerCase());
    });
    hot.render();
}

function updateTableData(data, id) {
    fetch('/update_tracker/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: data, id: id })
    })
}

const seriesLinks = document.querySelectorAll('a[onclick^="toggleTable("]');
seriesLinks.forEach(link => {
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
        $('#series-container ul li').each(function () {
            var serieName = $(this).find('a').text().toLowerCase();
            if (serieName.indexOf(searchTerm) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});

function showSeries(productName) {
    const allSerieTables = document.querySelectorAll('.series-table');
    allSerieTables.forEach(table => table.style.display = 'none');

    const selectedProductSeries = document.getElementById('series-' + productName);
    selectedProductSeries.style.display = 'block';

    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    const activeTab = Array.from(tabs).find(tab => tab.textContent.trim() === productName);
    if (activeTab) activeTab.classList.add('active');
}

function toggleTable(serieId) {
    const table = document.getElementById('serie-table-' + serieId);
    table.style.display = table.style.display === 'none' ? 'block' : 'none';
}

// Default behavior: show the first product's series by default
document.addEventListener('DOMContentLoaded', () => {
    const firstProduct = document.querySelector('.tab');
    if (firstProduct) {
        firstProduct.click();
    }
});

function getISOWeekNumber(d) {
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    var weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    return weekNo;
}

function getMonday(date) {
    const d = new Date(date);
    const day = d.getDay();
    const diff = (d.getDay() + 6) % 7;
    d.setDate(d.getDate() - diff);
    return d;
}

function toggleViewEdit() {
    const checkbox = document.getElementById('view-edit-checkbox');
    for (const key in hotInstances) {
        const hot = hotInstances[key];
        if (checkbox.checked) {
            hot.updateSettings({
                contextMenu: [
                    'add_child',
                    'detach_from_parent',
                    '---------',
                    'row_above',
                    'row_below',
                    '---------',
                    'remove_row',
                ],
                hiddenColumns: { columns: [], indicators: false }
            });
        } else {
            hot.updateSettings({
                contextMenu: false,
                hiddenColumns: { columns: [2, 3, 4, 5], indicators: false }
            });
        }
        hot.render();
    }
}

document.getElementById('view-edit-checkbox').addEventListener('change', function () {
    toggleViewEdit();
});

function areObjectsEqual(obj1, obj2) {
    return JSON.stringify(obj1) === JSON.stringify(obj2);
}

function collectChildren(row, seenChildren) {
    if (row.__children && Array.isArray(row.__children)) {
        row.__children.forEach(child => {
            seenChildren.push(child);
            collectChildren(child, seenChildren);
        });
    }
}

function removeChildren(sourceData) {
    let filteredData = [];
    let seenChildren = [];

    for (let row of sourceData) {
        let index = seenChildren.findIndex(child => areObjectsEqual(child, row));

        if (index !== -1) {
            seenChildren.splice(index, 1);
            continue;
        }
        filteredData.push(row);
        collectChildren(row, seenChildren);
    }

    return filteredData;
}