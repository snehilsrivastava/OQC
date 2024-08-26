CKEDITOR.on('dialogDefinition', function(event) {
    var dialogName = event.data.name;
    var dialogDefinition = event.data.definition;
    
    if (dialogName === 'image') {
        var uploadTab = dialogDefinition.getContents('Upload');
        var uploadButton = uploadTab.get('uploadButton');
        
        if (uploadButton) {
            uploadButton.hidden = true; // Hide the "Send it to the Server" button
            
            var fileInput = uploadTab.get('upload');
            
            fileInput.onChange = function() {
                var dialog = CKEDITOR.dialog.getCurrent();
                var file = dialog.getContentElement('Upload', 'upload').getInputElement().$.files[0];
                
                if (file) {
                    // Create a FormData object to hold the file
                    var formData = new FormData();
                    formData.append('ckeditor_image_upload', file);
                    
                    // Automatically use CKEditor's configured upload URL
                    var xhr = new XMLHttpRequest();
                    var uploadUrl = '/ckeditor_image_upload/'
                    xhr.open('POST', uploadUrl, true);
                    
                    xhr.send(formData);
                    
                    xhr.onload = function() {
                        if (xhr.status === 200) {
                            var response = JSON.parse(xhr.responseText);
                            if (response.url) {
                                dialog.selectPage('info');
                                dialog.setValueOf('info', 'txtUrl', response.url);
                            }
                        } else if (xhr.status === 422) {
                            var response = JSON.parse(xhr.responseText);
                            alert(response.error);
                        } else {
                            alert('Upload failed');
                        }
                    };
                }
            };
        }
    }
});