CKEDITOR.on('dialogDefinition', function(event) {
    var dialogName = event.data.name;
    var dialogDefinition = event.data.definition;

    if (dialogName === 'image') {
        var infoTab = dialogDefinition.getContents('info');
        var browseButton = infoTab.get('browse');

        // browseButton.onClick = function() {
        //     // Replace with your custom page URL
        //     var customPageUrl = '/server_media_browse/';
        //     window.open(customPageUrl, '_blank', 'toolbar=no,scrollbars=yes,resizable=yes,width=800,height=600');
        // };
        browseButton.label = 'Browse';
    }
});
