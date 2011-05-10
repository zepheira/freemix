/*global jQuery */
(function($) {
    $.fn.newViewDialog = function(create_url) {
        
        return this.each(function() {
            if (!create_url) {
                $(this).dialog({
                    autoOpen: false,
                    width: 500,
                    height: 500,
                    modal: true,
                    draggable: false,
                    resizable: false,
                    title: "Create a View"
                });
            } else {
                $(this).find("ul#canvas_chooser li a").each(function() {
                    $(this).attr("href", create_url + "&canvas=" + $(this).attr("id"));
                }).end()        
                .dialog("open");
            }
        });

    };
})(jQuery);