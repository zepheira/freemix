/*global jQuery */
(function($) {

    function loadEditor(evt) {
        var old = $("#dataset_metadata").html();
        $("#dataset_metadata").load($(this).attr("href"), function () {
            $(".dataset-edit-form-cancel").click(function() {
                $("#dataset_metadata").html(old);
                return false;
            });
            $("#dataset_metadata form").ajaxForm({"target": "#dataset_metadata"});
        });

        return false;
    }

    function setup() {
        $("#detail_edit_button").live('click', loadEditor);
        var url = $("#create_exhibit_button").attr("href");
        $("#create_exhibit_button").newExhibitDialog(url);

    }

    $(document).ready(setup);
})(jQuery);
