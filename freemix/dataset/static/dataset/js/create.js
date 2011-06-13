/*global jQuery */
(function($, Freemix) {
    $(document).ready(function() {

        var upload = new Freemix.UploadForm();
        var editor = new Freemix.DatasetEditor();
        $("#subnav").hide();
        upload.show();

    });

})(jQuery, jQuery.freemix);
