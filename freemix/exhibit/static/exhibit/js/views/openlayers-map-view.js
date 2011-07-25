/*global jQuery */
(function($, Freemix) {
    function OLDisplay(obj) {
	Freemix.mapViewLib.display(obj);
    };

    function OLGenerateExhibitHTML(obj) {
        return Freemix.mapViewLib.generateExhibitHTML(obj, "OLMap");
    };

    Freemix.view.addViewType({
        label: "Map",
        thumbnail: "/static/exhibit/img/map-icon.png",
        display: function(){OLDisplay(this)},
       	generateExhibitHTML: function(){return OLGenerateExhibitHTML(this)},
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
