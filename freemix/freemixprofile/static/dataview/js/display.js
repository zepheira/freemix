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

    Freemix.initialize = function(nextFn) {
        var model = Freemix.profile;
        var data;
        var dataProfile = model.dataProfile;

        Freemix.property.initializeFreemix();

        if (Freemix.data) {
            data = Freemix.data;
        } else {
            data = [];
            $.each(model.dataProfiles, function(inx, source) {
                if (source.url) {
                    data.push(source.url);
                }
            });
        }
        $.exhibit.initializeDatabase(data, function() {
            $("#canvas").generateExhibitHTML(model).createExhibit();
        });

        if (typeof nextFn != "undefined")
            nextFn();
    };


})(jQuery, jQuery.freemix);
