/*global jQuery */
 (function($, Freemix) {
    // Display the view's UI.
    function display() {
        var content = this.getContent();
        var root = Freemix.getTemplate("list-view-template");
        content.empty();
        root.appendTo(content);
        this._setupViewForm();
        this._setupLabelEditor();
        this._setupTitlePropertyEditor();
        this.findWidget().recordPager();
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
