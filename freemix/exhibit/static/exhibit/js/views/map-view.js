/*global jQuery */
(function($, Freemix) {
    Freemix.mapViewLib = {
        viewClass: "Map",
        propertyTypes: ["location"],
        label: "Map",
        thumbnail: "/static/exhibit/img/map-icon.png",

        config: {
            type: "map",
            title: undefined,
            titleLink: undefined,
            latlng: undefined,
            colorKey: undefined,
            metadata: []
        }

    };

    // Display the view's UI.
    Freemix.mapViewLib.display = function() {
        var content = this.getContent();
        var root = Freemix.getTemplate("map-view-template");
        content.empty();
        root.appendTo(content);
        this._setupViewForm();
        this._setupLabelEditor();
        this._setupTitlePropertyEditor();

        var latlng = content.find("#latlng_property");
        var points = Freemix.property.getPropertiesWithTypes(["location"]);
        this._setupSelectOptionHandler(latlng, "latlng", points);
        latlng.change();

        var color = content.find("#color_property");
        this._setupSelectOptionHandler(color, "color", Freemix.property.enabledProperties(), true);
        color.change();

        this.findWidget().recordPager();

    };

    Freemix.mapViewLib.generateExhibitHTML = function(config) {
        config = config || this.config;
        if (!config.latlng) {
            return $("<div ex:role='view' ex:viewClass='"+this.viewClass+"' ex:viewLabel='Location Missing'></div>");
        }
        var latlng = config.latlng;
        var colorKey = config.colorKey;
        var view = $("<div ex:role='view' ex:viewClass='"+this.viewClass+"'></div>");
        view.attr("ex:viewLabel", config.name);
        if (latlng) {
            view.attr("ex:latlng", '.' + latlng);
        }
        if (colorKey) {
            view.attr("ex:colorKey", '.' + colorKey);
        }
        this._renderFormats(view);

        var lens = $("<div class='map-lens' ex:role='lens' style='display:none'></div>");
        view.append(this._renderListLens(config));

        return view;
    };

})(window.Freemix.jQuery, window.Freemix);
