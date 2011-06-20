/*global jQuery */

 (function($, Freemix) {

    PICASA_BASE = "/http://picasaweb.google.com/data/feed/base/user/";
    TRANSFORMATION_BASE = "/transform/akara.augmented.json?url=";

    function isFacetCandidate(prop) {
        return (prop.values > 1 && prop.values + prop.missing != $.exhibit.database.getAllItemsCount());
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
        $.each(Freemix.property.enabledProperties(),
        function(name, property) {
            properties.push($.exhibit.getExpressionCount(property.expression(), property.label()));
        });
        properties.sort(sorter);
        return properties;
    }

    function createPropertyRow(property) {
        return $("<tr id='" + property.label + "'>" +
            "<td><input type='radio' name='property'/></td>" +
            "<td>" + property.label + "</td>" +
            "<td class='right'>" + property.values + "</td>" +
            "<td class='right'>" + property.missing + "</td></tr>")
        .hover(function() {
            $(this).addClass("ui-state-hover");
        },function() {
            $(this).removeClass("ui-state-hover");
        });


    }

    function createAlbumRow(album) {
        return $("<tr id='" + $(album).find('id').text() + "'>" +
            "<td><input type='radio' name='album'/></td>" +
            "<td>" + $(album).find('title').text() + "</td>" +
            "<td style='text-align:right;padding-right:16px'><img width='32' height='32' src='" +
            $(album).find('media\\:thumbnail').attr('url') + "'/></td></tr>")
        .hover(function() {
            $(this).addClass("ui-state-hover");
        },function() {
            $(this).removeClass("ui-state-hover");
        });


    }

    Freemix.facet.addFacetType({
        thumbnail: "/static/exhibit/img/image-facet.png",
        label: "Image",
        config: {
            type: "image",
            expression: "",
            albumTitle: "",
            album: "",
            showMissing: true,
            sortDirection: "forward",
            sortMode: "value",
            selection: undefined,
            scroll: true,
            fixedOrder: undefined
        },
        generateExhibitHTML: function() {
            var links = [TRANSFORMATION_BASE + this.config.album];
            $.exhibit.database._loadLinks(links, $.exhibit.database, function() {});
            return "<div ex:role='facet' ex:facetclass='Image' ex:expression='" + this.config.expression +
                "' ex:facetLabel='" + this.config.name +
                "' ex:image='.depiction' ex:tooltip='value' ex:height='122px'></div>";
        },
        showEditor: function(facetContainer) {
            var view = this;
            var properties = generatePropertyList();
            var editor = Freemix.getTemplate("image-facet-editor");
            var table = $("#add-facet-table tbody", editor).empty();
            $.each(properties,function(i, property) {
                var row = createPropertyRow(property).appendTo(table);
                $(":input", row).click(function() {
                    view.config.name = property.label;
                    view.config.expression = property.expression;
                    if (view.config.album) {
                        facetContainer.hidePopup();
                        facetContainer.addFacet(view);
                    }
                });
            });
            $("#user", editor).change(function(event) {
                var user = event.target.value;
                var editor = facetContainer.popupApi().elements.content;
                var atable = $("#album-facet-table tbody", editor).empty();
                atable.append($("<tr><td>Working...</td></tr>"));
                $.ajax({
                    type: "GET",
                    url: PICASA_BASE + user,
                    dataType: "xml",
                    error: function(req) {
                        var editor = facetContainer.popupApi().elements.content;
                        var atable = $("#album-facet-table tbody", editor).empty();
                        atable.append($("<tr><td>" + req.statusText + "</td></tr>"));
                    },
                    success: function(feed) {
                        var albums = $(feed).find('entry');
                        var editor = facetContainer.popupApi().elements.content;
                        var atable = $("#album-facet-table tbody", editor).empty();
                        $.each(albums,function(i, album) {
                            var row = createAlbumRow(album).appendTo(atable);
                            $(":input", row).click(function() {
                                view.config.album = $(album).find('link[rel=http://schemas.google.com/g/2005#feed] href');
                                view.config.albumTitle = $(album).find('title').text();
                                if (view.config.expression) {
                                    facetContainer.hidePopup();
                                    facetContainer.addFacet(view);
                                }
                            });
                        });
                    }
                });
            });
            facetContainer.setPopupContent(editor);

        },
        generateContent: function() {
            var count = $.exhibit.getExpressionCount(this.config.expression);
            return $("<div>Type: <em>" + this.config.type + "</em></div>" +
                "<div>Expression: <em>" + this.config.expression + "</em></div>" +
                "<div>Album: <em>" + this.config.albumTitle + "</em></div>" +
                "<div>Values: <em>" + count.values + "</em></div>" +
                "<div>Missing: <em>" + count.missing + "</em></div>");
        }
    });

})(jQuery, jQuery.freemix);
