/*global jQuery */
(function($, Freemix) {

    Freemix.exhibit.facetContainer = $.extend(true,{}, Freemix.exhibit.container, {
        id: "",
        findWidget: function() {
            if (!this._selector) {
                this._selector = $(".facet-container#" + this.id, Freemix.getBuilder());
            }
            return this._selector;
        },

        serialize: function() {
            var config = [];
            this.findWidget().find(".facet").each(function() {
                 var data = $(this).data("model");
                 config.push(data.serialize());
            });
            return config;
        },
        addFacet: function(facet) {
            facet.findWidget().appendTo(this.findWidget());
            facet.refresh();
            Freemix.getBuilder().on("freemix.show-builder", function() {
                facet.refresh();
            });

        },
        generateExhibitHTML: function() {
            var result = "";
             this.findWidget().find(".facet").each(function() {
                 result += $(this).data("model").generateExhibitHTML();
            });
            return result;
        },
        getPopupContent: function() {
            var fc = this;
                return $("<div class='chooser'></div>").freemixThumbnails(
                    Freemix.facet.types, Freemix.facet.prototypes,
                function(facetTemplate) {
                    var facet = Freemix.facet.createFacet({type: facetTemplate.config.type, name: facetTemplate.label});
                                facet.showEditor(fc);
                });
            },
        getPopupButton: function() {
            return this.findWidget().find(".create-facet-button");
        }
    });
    var context;
    Freemix.exhibit.facet = $.extend(true, {}, Freemix.exhibit.widget, {
        facetClass: Exhibit.ListFacet,
        findContainer: function() {
            return this.findWidget().parents(".facet-container");
        },
        generateWidget: function() {
            var facet = this;
            return $("<div class='facet ui-draggable' id='" + this.config.id + "'>" +
                "<div class='facet-header ui-state-default ui-helper-clearfix ui-dialog-titlebar' title='Click and drag to move to any other facet sidebar or to reorder facets'>" +
                "<span class='ui-icon ui-icon-grip-dotted-vertical'/>" +

                "<span class='label'>" + this.label + "</span>" +
                "<a href='#' class='delete-button ui-icon ui-icon-closethick' title='Delete this facet'/>" +
                "</div>" +
                "<div class='facet-body ui-widget-content'>" +
                "<div class='facet-content'></div>" +
                "<div class='facet-menu'><a href='#' title='Edit this facet'><span class='ui-icon ui-icon-pencil'/>edit</a></div>" +

                "</div></div>")
            .data("model", this)
            .find(".delete-button").click(function() {
                    facet.remove();
                    return false;
                }).end()
            .find(".facet-menu a").click(function() {

                    return false;
                });

        },

        refresh: function() {
            this.findWidget().find(".facet-content").empty().append(this.generateExhibitHTML());
            var exhibit = Freemix.getBuilderExhibit();
            this.facetClass.createFromDOM(this.findWidget().find(".facet-content div").get(0), null, exhibit._uiContext);

        },

        showEditor: function(facetContainer){
            facetContainer.hidePopup();
            facetContainer.addFacet(this);
        },
        generateExhibitHTML: function() {}
     });


     Freemix.facet = {
        createFacet: function(properties) {
            var props = $.extend({}, properties);
            if (!props.id) {
                props.id = $.make_uuid();
            }
            return $.extend(true, {},Freemix.facet.prototypes[properties.type], {config: props});
        },
        types: [],
        prototypes: {},
        addFacetType: function(content) {
            var type = content.config.type;
            Freemix.facet.types.push(type);

            var proto = $.extend(true, {},Freemix.exhibit.facet,content);
            if (content.propertyTypes) {
                proto.propertyTypes = content.propertyTypes;
            }
            Freemix.facet.prototypes[type]=proto;
        },
        getFacetContainer: function(id) {
          return $(".facet-container#" + id, Freemix.getBuilder()).data("model");
        }
    };

})(window.Freemix.jQuery, window.Freemix);
