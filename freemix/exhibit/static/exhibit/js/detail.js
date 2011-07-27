/*global jQuery */
(function($) {

    var dialog;

    function setupForm(dialog) {
            $(".exhibit-edit-form-cancel", dialog).click(function() {
                dialog.dialog("close");
                return false;
            });

            $("form", dialog).ajaxForm({
                "success": function(response, status, xhr, form) {
                    var html = $(response);
                    if (html.has("form").length > 0) {
                        dialog.html(html);
                        setupForm(dialog);
                    } else {
                        $("#exhibit_metadata").html(html);
                        dialog.dialog("close");
                        dialog.empty();
                    }

                }
            });
    }

    function loadEditor(evt) {

        var url = $(this).attr("href");
        dialog.dialog("open");
        dialog.load(url, function(response, status, xhr) {
            setupForm(dialog)
        });
        return false;

    }

    function setupEditDetails() {
        dialog = $('<div style="display:hidden"></div>').appendTo('body');

        dialog.dialog({
            width: 500,
            height: "auto",
            modal: true,
            draggable: false,
            resizable: false,
            autoOpen: false,
            title: "Edit Data View Details"
        });

        $("#detail_edit_button").live("click", loadEditor);
    }


    function setup() {
        setupEditDetails();
    }

    $(document).ready(setup);
})(jQuery);
