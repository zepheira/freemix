/*global jQuery */
 (function($, Freemix) {

      // Display the view's UI.
     function display() {
         var content = this.getContent();
         var root = Freemix.getTemplate("scatterplot-view-template");
         var model = this;
         content.empty();
         root.appendTo(content);

         model._setupViewForm();
         model._setupLabelEditor();
         model._setupTitlePropertyEditor();

         var numbers = Freemix.property.getPropertiesWithTypes(["number"]);

         var xaxis = content.find("#xaxis_property");
         var yaxis = content.find("#yaxis_property");

         model._setupSelectOptionHandler(xaxis, "xaxis", numbers);
         model._setupSelectOptionHandler(yaxis, "yaxis", numbers);
         xaxis.change();
         yaxis.change();
         model.findWidget().recordPager();

     }

    function generateExhibitHTML(config) {
        config = config || this.config;

        if (typeof config.xaxis === "undefined" || typeof config.yaxis === "undefined") {
            return $('<div ex:role="view" ex:viewLabel="Axis Missing"></div>');
        }

        var xaxis = config.xaxis;
        var yaxis = config.yaxis;
        if (xaxis && yaxis) {
            var minx = 0;
            var maxx = 0;
            var miny = 0;
            var maxy = 0;
            var database = Freemix.exhibit.database;
            var recordIds = database.getAllItems().toArray();
            for (var i = 0; i < recordIds.length; i++) {
                var id = recordIds[i];
                var record = database.getItem(id);
                var x = parseFloat(record[xaxis]);
                var y = parseFloat(record[yaxis]);
                if (minx > x || i === 0) {
                    minx = x;
                }
                if (maxx < x || i === 0) {
                    maxx = x;
                }
                if (miny > y || i === 0) {
                    miny = y;
                }
                if (maxy < y || i === 0) {
                    maxy = y;
                }
            }
            if (maxx - minx <= 1 && maxx - minx > 0) {
                return $("<div ex:role='view' ex:viewLabel='Unsupported Range Values'></div>");
            }
            if (maxy - miny <= 1 && maxy - miny > 0) {
                return $("<div ex:role='view' ex:viewLabel='Unsupported Range Values'></div>");
            }
        }

        var view = $("<div ex:role='view' ex:viewClass='Exhibit.ScatterPlotView' ex:viewLabel='" + config.name + "'></div>");
        var props = Freemix.property.enabledProperties();
        if (xaxis) {
            view.attr("ex:x", props[xaxis].expression());
            view.attr("ex:xLabel", props[xaxis].label());
        }
        if (yaxis) {
            view.attr("ex:y", props[yaxis].expression());
            view.attr("ex:yLabel", props[yaxis].label());
        }

        var lens = $("<div class='scatterplot-lens' ex:role='lens' style='display:none'></div>");
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
        lens.append(title);
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
    }

    Freemix.view.addViewType({
        propertyTypes: ["number", "currency"],

        label: "Scatter Plot",
        thumbnail: "/static/exhibit/img/scatterplot-icon.png",
        display: display,
        generateExhibitHTML: generateExhibitHTML,

        config: {
            type: "scatterplot",
            title: undefined,
            titleLink: undefined,
            xaxis: undefined,
            yaxis: undefined,
            metadata: []
        }
    });

})(window.Freemix.jQuery, window.Freemix);
