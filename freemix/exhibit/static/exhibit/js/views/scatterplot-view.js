/*global jQuery */
 (function($, Freemix) {

      // Display the view's UI.
     function display() {
         var content = this.getContent();
         var root = Freemix.getTemplate("scatterplot-view-template");
         var model = this;
         content.empty();
         root.appendTo(content);
         this.findWidget().recordPager(
             function(row, model, metadata) {

                 $("<td class='inner'></td>").insertAfter(row.find('td.visible')).createChildCheck({
                     radio: true,
                     checked:  model.config['yaxis'] === metadata.property,
                     change: function() {
                         if ($(this).is(":checked")) {
                              model.config['yaxis'] = metadata.property;
                         }
                     },
                     name: 'yaxis'
                 });

                 $("<td class='inner'></td>").insertAfter(row.find("td.visible")).createChildCheck({
                     radio: true,
                     checked:  model.config['xaxis'] === metadata.property,
                     change: function() {
                         if ($(this).is(":checked")) {
                              model.config['xaxis'] = metadata.property;
                         }
                     },
                     name: 'xaxis'
                 });

                 if (Freemix.property.propertyHasType(metadata.property, "url")) {
                     $("<td class='inner title-link-option'></td>").insertAfter(row.find('td.visible')).createChildCheck({
                         radio: true,
                         checked: model.config.titleLink === metadata.property,
                         change: function() {
                             if ($(this).is(":checked")) {
                                 model.config.titleLink = metadata.property;
                             }
                         },
                         name: 'titleLink'
                     });
                 } else {
                     $('<td class="inner title-link-option"><input type="radio" disabled="true" /></td>').insertAfter(row.find('td.visible'));
                 }

                 $("<td class='inner'></td>").insertAfter(row.find('td.visible')).createChildCheck({
                     radio: true,
                     checked: model.config.title === metadata.property,
                     change: function() {
                         if ($(this).is(":checked")) {
                             model.config.title = metadata.property;
                             $('.view-content:visible .title-link-option').fadeIn();
                         }
                     },
                     name: 'title'
                 });
            }
         );
         $('#clear-title').bind('click', function() {
             model.config.title = null;
             $('.view-content:visible .title-link-option').fadeOut();
         });
         $('#clear-title-link').bind('click', function() {
             model.config.titleLink = null;
         });
         if (typeof model.config.title !== "undefined" && model.config.title != null) {
             $('.view-content:visible .title-link-option').show();
         }
         if (typeof model.config.xaxis === "undefined") {
             $('.required-setting[rel=property-xaxis]').show();
             $('.required-setting[rel=property-xaxis]:visible').bind('mouseover', function() {
                 $('#'+$(this).attr('rel')).addClass('ui-state-highlight');
             }).bind('mouseout', function() {
                 $('#'+$(this).attr('rel')).removeClass('ui-state-highlight');
             });
             $('input[name=xaxis]').bind('change', function() {
                 $('.required-setting[rel=property-xaxis]:visible').hide();
             });
         } else {
             $('.required-setting[rel=property-xaxis]:visible').hide();
         }
         if (typeof model.config.yaxis === "undefined") {
             $('.required-setting[rel=property-yaxis]').show();
             $('.required-setting[rel=property-yaxis]:visible').bind('mouseover', function() {
                 $('#'+$(this).attr('rel')).addClass('ui-state-highlight');
             }).bind('mouseout', function() {
                 $('#'+$(this).attr('rel')).removeClass('ui-state-highlight');
             });
             $('input[name=yaxis]').bind('change', function() {
                 $('.required-setting[rel=property-yaxis]:visible').hide();
             });
         } else {
             $('.required-setting[rel=property-yaxis]:visible').hide();
         }
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
