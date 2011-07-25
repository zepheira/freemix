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

        getConfigList: function() {
            var config = [];
            this.findWidget().find(".facet").each(function() {
                 var data = $(this).data("model");
                 config.push($.extend(true, {}, data.config));
            });
            return config;
        },
        addFacet: function(facet) {
            facet.findWidget().appendTo(this.findWidget());
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

    Freemix.exhibit.facet = $.extend(true, {}, Freemix.exhibit.widget, {
        findContainer: function() {
            return this.findWidget().parents(".facet-container");
        },
        generateWidget: function() {
            var facet = this;
            return $("<div class='facet ui-draggable' id='" +
                this.config.id + "'><div class='facet-header ui-state-default ui-helper-clearfix ui-dialog-titlebar' title='Click and drag to move to any other facet sidebar or to reorder facets'><span class='label'>" + this.config.name +
                "</span><span class='popup-button ui-icon ui-icon-triangle-1-s'/></div>" +
                "<div class='facet-content ui-widget-content'></div></div>")
            .data("model", this)
            .find(".popup-button").freemixPopupButton("Edit Facet", function() {
                return facet.getPopupContent();
            }).end()
            .find(".facet-content").append(this.generateContent()).end();
        },
        generateContent: function() {
            return $("<span>Type: <em>" + this.config.type + "</em></span>");
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
            var facet = $.extend(true, {},Freemix.facet.prototypes[properties.type], {config: props});
            return facet;
        },
        types: [],
        prototypes: {},
        addFacetType: function(content) {
            var type = content.config.type;
            Freemix.facet.types.push(type);
            Freemix.facet.prototypes[type]= $.extend(true, {},Freemix.exhibit.facet,content);
        },
        getFacetContainer: function(id) {
          return $(".facet-container#" + id, Freemix.getBuilder()).data("model");
        }
    };

})(window.Freemix.jQuery, window.Freemix);
