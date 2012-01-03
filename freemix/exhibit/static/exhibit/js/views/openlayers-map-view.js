/*global jQuery */
(function($, Freemix) {
    function OLDisplay(obj) {
        Freemix.mapViewLib.display(obj);
    }

    function OLGenerateExhibitHTML(obj) {
        return Freemix.mapViewLib.generateExhibitHTML(obj, "OLMap");
    }

    Freemix.view.addViewType({
        facetClass: Exhibit.OLMapView,
        propertyTypes: ["location"],
        label: "Map",
        thumbnail: "/static/exhibit/img/map-icon.png",
        display: function(){OLDisplay(this)},
       	generateExhibitHTML: function(config){return OLGenerateExhibitHTML(config || this.config)},
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
