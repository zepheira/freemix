/*global jQuery */
(function($, Freemix) {

    $.fn.generateExhibitHTML = function(model) {
        return this.each(function() {
            var root = $(this);
            if (model.text) {

                $.each(model.text, function(key, value) {
                    var id = $(this).attr("id");
                    root.find("#" + key).text(value);
                });
                if (model.text.title) {
                    document.title = model.text.title;
                }
            }
            root.find(".view-container").each(function() {
                var id = $(this).attr("id");
                var container = $("<div class='view-panel' ex:role='viewPanel'></div>");
                $.each(model.views[id], function() {
                    var view = Freemix.view.createView(this);
                    container.append(view.generateExhibitHTML());
                });

                root.find(".view-container#" + id).append(container);
            });

            $.each(model.facets, function(container, facets) {
                $.each(facets, function() {
                    var facet = Freemix.facet.createFacet(this);
                    root.find(".facet-container#" +container).append(facet.generateExhibitHTML());
                });
            });
            $('body').trigger('initialized.exhibit');
        });
    };

    function run_init(nextFn) {
        Freemix.property.initializeFreemix();

        var data = Freemix.data || [$("link[rel='exhibit/data']").attr("href")];

        Freemix.exhibit.initializeDatabase(data, function() {
            $("#canvas").generateExhibitHTML(Freemix.profile).createExhibit();
        });

        if (typeof nextFn != "undefined") {
            nextFn();
        }
    }

    Freemix.initialize = function(nextFn) {
        if (Freemix.data_profile) {
            run_init(nextFn);

        } else {
            var dp_url = $("link[rel='freemix/dataprofile']").attr("href");
            $.ajax({
                url: dp_url,
                type: "GET",
                dataType: "json",
                success: function(dp) {
                    Freemix.data_profile=dp;
                    run_init(nextFn);
                }
            });
        }
    };


})(window.Freemix.jQuery, window.Freemix);
