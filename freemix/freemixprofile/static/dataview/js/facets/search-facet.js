/*global jQuery */
(function($, Freemix) {

    Freemix.facet.addFacetType({
        thumbnail: "/static/dataview/img/search-facet.png",
        label: "Search",
        config: {
            type: "search"
        },
        generateExhibitHTML: function () {
            return "<div ex:role='facet' ex:facetClass='TextSearch' ex:facetLabel='" + this.config.name + "'></div>";
        }
    });

})(jQuery, jQuery.freemix);
