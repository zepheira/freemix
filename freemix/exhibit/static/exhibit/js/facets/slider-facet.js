/*global jQuery */
 (function($, Freemix) {

    function isFacetCandidate(prop) {
        return (prop.values > 1 && prop.values + prop.missing != Freemix.exhibit.database.getAllItemsCount());
    }

    function simpleSort(a, b) {
        if (a.missing == b.missing) {
            return a.values - b.values;
        } else {
            return a.missing - b.missing;
        }
    }

    function sorter(a, b) {
        var aIsCandidate = isFacetCandidate(a);
        var bIsCandidate = isFacetCandidate(b);

        if ((aIsCandidate && bIsCandidate) || (!aIsCandidate && !bIsCandidate)) {
            return simpleSort(a, b);
        }
        return bIsCandidate ? 1: -1;
    }


    function generatePropertyList() {
        var properties = [];
        $.each(Freemix.property.getPropertiesWithTypes(["number", "currency"]),
        function(name, property) {
            properties.push(Freemix.exhibit.getExpressionCount(property.expression(), property.label()));
        });
        properties.sort(sorter);
        return properties;
    }

    function createPropertyRow(property) {
       return  $("<tr id='" + property.label + "' class='ui-state-default'>" +
            "<td>" + property.label + "</td>" +
            "<td class='right'>" + property.values + "</td>" +
            "<td class='right'>" + property.missing + "</td></tr>");
    }

    Freemix.facet.addFacetType({
        facetClass: Exhibit.SliderFacet,
        propertyTypes: ["number", "currency"],

        thumbnail: "/static/exhibit/img/slider-facet.png",
        label: "Slider",
        config: {
            type: "Slider",
	    expression: "",	    
	    height: "50px"
        },
        generateExhibitHTML: function() {
            return "<div ex:role='facet' ex:facetClass='Slider' ex:histogram='true' ex:horizontal='true' ex:height='50px' ex:expression='" + this.config.expression +
                "' ex:facetLabel='" + this.config.name + "'></div>";
        },
        showEditor: function(facetContainer) {
            var view = this;
            var properties = generatePropertyList();
            var editor = Freemix.getTemplate("list-facet-editor");
            var table = $("#add-facet-table tbody", editor).empty();
            $.each(properties,
            function(i, property) {
                createPropertyRow(property).click(function() {
                    view.config.name = property.label;
                    view.config.expression = property.expression;
                    facetContainer.hidePopup();
                    facetContainer.addFacet(view);
                }).appendTo(table);
            });

            facetContainer.setPopupContent(editor);

        },

        serialize: function() {
            return $.extend(true, {}, this.config);
        }
    });
})(window.Freemix.jQuery, window.Freemix);
