/*global jQuery */
 (function($, Freemix) {

     // Display the view's UI.
     function display() {
         var content = this.getContent();
         var root = Freemix.getTemplate("timeline-view-template");
         content.empty();
         root.appendTo(content);
         var model = this;

         model._setupViewForm();
         model._setupLabelEditor();
         model._setupTitlePropertyEditor();

         var start = content.find("#start_property");
         var end = content.find("#end_property");
         var color = content.find("#color_property");
         var top_band = content.find("#top-band-unit");
         var bottom_band = content.find("#bottom-band-unit");

         top_band.change(function() {
             var value = $(this).val();
             model.config.topBandUnit = $(this).val();
         }).val(model.config.topBandUnit);

         bottom_band.change(function() {
             var value = $(this).val();
             model.config.bottomBandUnit = $(this).val();
         }).val(model.config.bottomBandUnit);

         if (!top_band.val()) {
             top_band.get(0).options[0].selected = true;
             top_band.change();
         }
         if (!bottom_band.val()) {
             bottom_band.get(0).options[0].selected = true;
             bottom_band.change();
         }

         var dates = Freemix.property.getPropertiesWithTypes(model.propertyTypes);
         var colors = Freemix.property.enabledProperties();

         model._setupSelectOptionHandler(start, "startDate", dates);
         model._setupSelectOptionHandler(end, "endDate", dates, true);
         model._setupSelectOptionHandler(color, "colorKey", colors, true);

         start.change();
         end.change();
         color.change();

         model.findWidget().recordPager();

     }

    function generateExhibitHTML(config) {
        function expression(prop) {
            return "." + prop;
        }
        config = config || this.config;
        if (!config.startDate) {
            return $("<div ex:role='view' ex:viewLabel='Range Missing'></div>");
        }
        var props = Freemix.property.enabledProperties();
        var colorKey = config.colorKey;
        var view = $("<div ex:role='view' ex:viewClass='Timeline' ex:viewLabel='" + config.name + "'></div>");
        if (colorKey) {
            view.attr("ex:colorKey", expression(colorKey));
        }
        if (config.name) {
            view.attr("ex:label", config.name);
        }
        if (config.title) {
            view.attr("ex:eventLabel", expression(config.title));
        }
        if (config.startDate) {
            view.attr("ex:start", expression(config.startDate));
        }
        if (config.endDate) {
            view.attr("ex:end", expression(config.endDate));
        }
        if (config.topBandUnit) {
            view.attr("ex:topBandUnit", config.topBandUnit);
        }
        if (config.bottomBandUnit) {
            view.attr("ex:bottomBandUnit", config.bottomBandUnit);
        }
        if (config.topBandPixelsPerUnit) {
            view.attr("ex:topBandPixelsPerUnit", expression(config.topBandPixelsPerUnit));
        }
        if (config.bottomBandPixelsPerUnit) {
            view.attr("ex:bottomBandUnitsPerPixel", expression(config.bottomBandPixelsPerUnit));
        }

        var lens = $("<div class='timeline-lens ui-widget-content' ex:role='lens' style='display:none'></div>");
        var title = $("<div class='exhibit-title ui-widget-header'></div>");
        if (this.config.title) {
            var html = "<span ex:content='" + expression(this.config.title) + "' ></span>";
            if (this.config.titleLink) {
                html += "&nbsp;<a ex:href-content='" + expression(this.config.titleLink) + "' target='_blank'>(link)</a>";
            }
            title.append(html);
            var formats = "item {title:expression(" + expression(this.config.title) + ")}";
            view.attr("ex:formats", formats);
        }
        lens.append(title);
        var table = $("<table class='property-list-table exhibit-list-table'></table>");
        $.each(this.config.metadata,
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
    }

    Freemix.view.addViewType({
        propertyTypes: ["date"],
        label: "Timeline",
        thumbnail: "/static/exhibit/img/timeline-icon.png",
        display: display,
        generateExhibitHTML: generateExhibitHTML,

        config: {
            type: "timeline",
            title: undefined,
            titleLink: undefined,
            colorKey: undefined,
            startDate: undefined,
            endDate: undefined,
            topBandUnit: "auto",
            topBandPixelsPerUnit: undefined,
            bottomBandUnit: "auto",
            bottomBandPixelsPerUnit: undefined,
            metadata: []
        }
    });

})(window.Freemix.jQuery, window.Freemix);
