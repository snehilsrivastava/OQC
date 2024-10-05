CKEDITOR.editorConfig = function( config ) {
    config.versionCheck = false;
    config.allowedContent = true;
    config.autoParagraph = false;
    config.enterMode = CKEDITOR.ENTER_DIV; 
    config.shiftEnterMode = CKEDITOR.ENTER_DIV;
    config.width = '665px';
    config.skin = 'moono-lisa';
    config.removeDialogTabs = 'image:Link;image:advanced';
    config.toolbar = [
        { items: ['Table', 'Image'] }
    ];
    config.filebrowserUploadUrl = '/ckeditor_image_upload/';
    config.filebrowserBrowseUrl = '/server_media_browse/';
    config.filebrowserImageBrowseUrl = '/server_media_browse/?type=Images';
};