/*global jQuery, window, alert, console */
 (function($) {

    $.freemix = {
        getTemplate: function(template) {
            return $($("#templates div#" + template).html());
        }
    };




    $.fn.freemixStepTabs = function(option, selector) {

        return this.each(function() {
            if (option === "select") {
                $(this).find("a[href='" + selector + "']").trigger("tab-select");
            } else if (option == "incomplete") {
                $(this).find("a[href='" + selector + "']").parent("li").nextAll().find("a").addClass("step-disabled");
            } else if (option == "complete") {
                $(this).find(".step-disabled").removeClass("step-disabled");
            } else {
                var tabset = $(this);
                var callbacks = option||{};
                tabset.find("li>a").each(function() {
                    var a = $(this);
                    var sel = a.attr("href");
                    $(sel).addClass("tab-contents");
                    var callback = callbacks[sel.substring(1)]||function(){};
                    a.bind("tab-select", function() {
                        if (!a.hasClass("tab-selected")) {
                            $(".tab-contents").hide().removeClass("tab-selected");

                            tabset.find("a").removeClass("step-completed step-selected");
                            a.addClass("step-selected").parent("li").prevAll().find("a").addClass("step-completed");

                            $(sel).addClass("tab-selected").show();
                            (function() {
                                callback();

                            })();

                        }
                    }).click(function() {
                        a.trigger("tab-select");
                        return false;
                    });

                });
            }
        });
    };



})(jQuery);
