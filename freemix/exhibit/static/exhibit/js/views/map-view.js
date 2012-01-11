/*global jQuery */
(function($, Freemix) {
    Freemix.mapViewLib = {};

    // Display the view's UI.
    Freemix.mapViewLib.display = function(o) {
        var content = o.getContent();
        var root = Freemix.getTemplate("map-view-template");
        content.empty();
        root.appendTo(content);
        o._setupViewForm();
        o._setupLabelEditor();
        o._setupTitlePropertyEditor();

        var latlng = content.find("#latlng_property");
        var points = Freemix.property.getPropertiesWithTypes(["location"]);
        o._setupSelectOptionHandler(latlng, "latlng", points);
        latlng.change();

        var color = content.find("#color_property");
        o._setupSelectOptionHandler(color, "color", Freemix.property.enabledProperties(), true);
        color.change();

        o.findWidget().recordPager();

    };

    Freemix.mapViewLib.generateExhibitHTML = function(config, viewClass) {
        if (!config.latlng) {
            return $("<div ex:role='view' ex:viewClass='"+viewClass+"' ex:viewLabel='Location Missing'></div>");
        }
        var latlng = config.latlng;
        var colorKey = config.colorKey;
        var view = $("<div ex:role='view' ex:viewClass='"+viewClass+"' ex:viewLabel='" + config.name + "'></div>");
        if (latlng) {
            view.attr("ex:latlng", '.' + latlng);
        }
        if (colorKey) {
            view.attr("ex:colorKey", '.' + colorKey);
        }
        var lens = $("<div class='map-lens' ex:role='lens' style='display:none'></div>");
        var props = Freemix.property.enabledProperties();

        var title = $("<div class='exhibit-title ui-widget-header'></div>");
        if (config.title) {
            var html = "<span ex:content='" + props[config.title].expression() + "' ></span>";
            if (config.titleLink) {
                html += "&nbsp;<a ex:href-content='" + props[config.titleLink].expression() + "' target='_blank'>(link)</a>";
            }
            title.append(html);

            var formats = "item {title:expression(" + props[config.title].expression() + ")}";
            view.attr("ex:formats", formats);
        }

        var table = $("<table class='property-list-table exhibit-list-table'></table>");
        $.each(config.metadata,
        function(index, metadata) {
            var property = metadata.property;
            var identify = props[property];
            if (!metadata.hidden && identify) {
                var label = identify.label();
                $("<tr class='exhibit-property'><td class='exhibit-label'>" + label + "</td><td class='exhibit-value'>" + Freemix.exhibit.renderProperty(metadata) + "</td></tr>").appendTo(table);
            }

        });
        lens.append(table).appendTo(view);
        return view;
    };

})(window.Freemix.jQuery, window.Freemix);
