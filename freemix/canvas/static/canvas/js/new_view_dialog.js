/*global jQuery */
(function($) {
    $.fn.newExhibitDialog = function(url) {

        return this.each(function() {
            $(this).click(function() {
                var dialog = $('<div style="display:hidden"></div>').appendTo('body');

                dialog.load(url, function (responseText, textStatus, XMLHttpRequest) {
                    dialog.dialog({
                        width: 500,
                        height: 500,
                        modal: true,
                        draggable: false,
                        resizable: false,
                        title: "Create a View"
                    });
                });
                return false;
            });
        });

    };
})(jQuery);