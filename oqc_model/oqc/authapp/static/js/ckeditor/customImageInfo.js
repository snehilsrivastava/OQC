CKEDITOR.on('dialogDefinition', function(event) {
    var dialogName = event.data.name;
    var dialogDefinition = event.data.definition;

    if (dialogName === 'image') {
        var infoTab = dialogDefinition.getContents('info');
        var browseButton = infoTab.get('browse');
        browseButton.label = 'Browse';
    }
    
    setTimeout(function() {
        let image_preview_parent = document.querySelector('.ImagePreviewBox a').parentElement;
        const old_text_node = Array.from(image_preview_parent.childNodes).find(node => node.nodeType === 3 && node.nodeValue.trim() !== '');
        let new_span = document.createElement('span');
        new_span.textContent = 'This is a preview of image size with the text size as it would look in the report.';
        let preview_img = image_preview_parent.querySelector('img');
        let img_width = preview_img.getAttribute('style');
        new_span.style.width = img_width;
        image_preview_parent.replaceChild(new_span, old_text_node);
    }, 10);
});