/*global jQuery */
(function($) {


    function setupForm(dialog) {
        var form = dialog.find("form");

        form.ajaxForm({
            "target": dialog,
            "success": function() {
                if (dialog.has(".create_success").length > 0) {
                    dialog.append("<div>Redirecting...</div>");
                    window.location = dialog.find("a.create_success").attr("href");
                } else {
                    setupForm(dialog);
                }
                return false;

            }
        });
    }

    function setupSaveButton() {
        var dialog = $('<div style="display:hidden"></div>').appendTo('body');

        dialog.dialog({
            width: 500,
            height: "auto",
            modal: true,
            draggable: false,
            resizable: false,
            autoOpen: false,
            title: "Create a New Shared Key"
        });

        $("a.exhibit_share").click(function() {
                var url = $(this).attr("href");
                dialog.dialog("open");
                dialog.load(url, function (responseText, textStatus, XMLHttpRequest) {
                    setupForm(dialog);

                    $(".shared-key-form-cancel").click(function() {dialog.dialog("close");});
                });
                return false;
            });

    }

    $(document).ready(setupSaveButton)

})(jQuery);