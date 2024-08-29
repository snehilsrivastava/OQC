let urlParams = new URLSearchParams(window.location.search);
let CKEditorFuncNum = urlParams.get('CKEditorFuncNum');
let selectedFile;
function selectFile() {
    if (selectedFile) {
        if (CKEditorFuncNum) {
            window.opener.CKEDITOR.tools.callFunction(CKEditorFuncNum, selectedFile);
            window.close();  // Close the file manager window after selection
        } else {
            alert('CKEditor callback function not found.');
        }
    } else {
        alert('No file selected.');
    }
};

function previewImg(url, name) {
    let img = document.getElementById('previewImg');
    img.src = url;
    img.alt = name;
    selectedFile = url;
}

document.addEventListener('DOMContentLoaded', () => {
    const dateInput = document.getElementById('date');
    const sortCheckbox = document.getElementById('sort_order');

    // Get existing URL parameters, including CKEditorFuncNum
    let urlParams = new URLSearchParams(window.location.search);
    let CKEditorFuncNum = urlParams.get('CKEditorFuncNum');

    function updateFilter() {
        const date = dateInput.value;
        const sortOrder = sortCheckbox.checked ? 'asc' : 'desc';

        // Update or add the filter parameters
        urlParams.set('date', date);
        urlParams.set('order', sortOrder);

        // Ensure CKEditorFuncNum is preserved in the URL
        if (CKEditorFuncNum) {
            urlParams.set('CKEditorFuncNum', CKEditorFuncNum);
        }

        // Update the URL with all parameters
        window.location.search = urlParams.toString();
    }

    dateInput.addEventListener('change', updateFilter);
    sortCheckbox.addEventListener('change', updateFilter);
});