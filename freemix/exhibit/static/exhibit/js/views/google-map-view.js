/*global jQuery */
(function($, Freemix) {
    function GoogleDisplay(obj) {
	Freemix.mapViewLib.display(obj);
    };

    function GoogleGenerateExhibitHTML(obj) {
        return Freemix.mapViewLib.generateExhibitHTML(obj, "Map");
    };

    Freemix.view.addViewType({
        propertyTypes: ["location"],
        label: "Map",
        thumbnail: "/static/exhibit/img/map-icon.png",
        display: function(){GoogleDisplay(this)},
        generateExhibitHTML: function(){return GoogleGenerateExhibitHTML(this)},
        config: {
            type: "map",
            title: undefined,
            titleLink: undefined,
            latlng: undefined,
            colorKey: undefined,
            metadata: []
        }
    });

})(window.Freemix.jQuery, window.Freemix);
