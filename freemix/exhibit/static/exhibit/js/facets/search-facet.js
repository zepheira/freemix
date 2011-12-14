/*global jQuery */
(function($, Freemix) {

    Freemix.facet.addFacetType({
        facetClass: Exhibit.TextSearchFacet,
        thumbnail: "/static/exhibit/img/search-facet.png",
        label: "Search",
        config: {
            type: "search"
        },
        generateExhibitHTML: function () {
            return "<div ex:role='facet' ex:facetClass='TextSearch' ex:facetLabel='" + this.config.name + "'></div>";
        },
        serialize: function() {
            return $.extend(true, {}, this.config);
        }
    });

})(window.Freemix.jQuery, window.Freemix);
