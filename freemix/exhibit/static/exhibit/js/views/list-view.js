/*global jQuery */
 (function($, Freemix) {
    // Display the view's UI.
    function display() {
        var content = this.getContent();
        var root = Freemix.getTemplate("list-view-template");
        content.empty();
        root.appendTo(content);
        var config = this.config;
        this.findWidget().recordPager(
            function(row, model, metadata) {
                 if (Freemix.property.propertyHasType(metadata.property, "url")) {
                     $("<td class='inner title-link-option'></td>").insertAfter(row.find("td.visible")).createChildCheck({
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
                     $('<td class="inner title-link-option"><input type="radio" disabled="true" /></td>').insertAfter(row.find("td.visible"));
                 }

                 $("<td class='inner'></td>").insertAfter(row.find("td.visible")).createChildCheck({
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
            config.title = null;
            $('.view-content:visible .title-link-option').fadeOut();
        });
        $('#clear-title-link').bind('click', function() {
            config.titleLink = null;
        });
        if (typeof config.title !== "undefined" && config.title != null) {
            $('.view-content:visible .title-link-option').show();
        }
    }

    function generateExhibitHTML(config) {
        config = config || this.config;
        var view = $("<div ex:role='view' ex:viewLabel='" + config.name + "'></div>");
        var props = Freemix.property.enabledProperties();

        var lens = $("<div ex:role='lens' style='display:none'></div>");
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
        thumbnail: "/static/exhibit/img/list-icon.png",
        label: "List",
        display: display,
        generateExhibitHTML: generateExhibitHTML,
        config: {
            type: "list",
            title: undefined,
            titleLink: undefined,
            metadata: []
        }
    });

})(window.Freemix.jQuery, window.Freemix);
