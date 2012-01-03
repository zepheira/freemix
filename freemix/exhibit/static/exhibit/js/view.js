/*global jQuery */
(function($, Freemix) {


    Freemix.exhibit.viewContainer = $.extend(true, {}, Freemix.exhibit.container,{
        id: "",
        findWidget: function() {
            return $(".view-container#" + this.id, Freemix.getBuilder());
        },
        getContent: function() {
            return $(".view-content", this.findWidget());
        },
        generateExhibitHTML: function() {
            var viewPanel = $("<div class='view-panel' ex:role='viewPanel'></div>");
            $("ul.view-set>li", this.findWidget()).each(function() {
                // TODO: the new view icon should be moved out of the list
                if (!$(this).hasClass("create-view")) {
                    var view = $(this).data("model");
                    viewPanel.append(view.generateExhibitHTML());
                }
            });
            return viewPanel;
        },
        serialize: function() {
            var config = [];
            $("ul.view-set>li", this.findWidget()).each(function() {
                if (!$(this).hasClass("create-view")) {
                    var view = $(this).data("model");
                    config.push(view.serialize());
                }
            });
            return config;
        },
        addView: function(view) {
            $('.view-set li.create-view', this.findWidget()).before(view.findWidget());
            view.select();
        },
        getSelected: function() {
            return this.findWidget().find(".view-set>li.ui-state-active");
        },
        getPopupContent: function() {
            var fc = this;
            return $("<div class='chooser'></div>")
                .freemixThumbnails(Freemix.view.types, Freemix.view.prototypes, function(viewTemplate) {
                    var view = Freemix.view.createView({type: viewTemplate.config.type, name: viewTemplate.label});
                    view.showEditor(fc);
                });
        },
        getPopupButton: function() {
            return this.findWidget().find(".create-view-button");
        }
    });

    Freemix.exhibit.view = $.extend(true, {}, Freemix.exhibit.widget, {
        propertyTypes: ["text", "image", "currency", "url", "location", "date", "number"],
        getContainer: function() {
            if (!this._container) {
                this._container = this.findWidget().parents(".view-container");
            }
            return this._container;
        },
        getContent: function() {
            return this.getContainer().data("model").getContent();
        },
        generateWidget: function() {
             var view = this;
             var widget =  $("<li id='" + view.config.id +
                            "' class='view button button-icon-left ui-state-default'><span class='popup-button ui-icon ui-icon-triangle-1-s'/><span class='label'>" +
                            view.config.name + "</span></li>")
                .data("model", view)
                .hover(function() {$(this).addClass('ui-state-hover');}, function() {$(this).removeClass('ui-state-hover');})
                .click(function() {
                    if (!$(this).hasClass("ui-state-active")) {
                        $(this).data("model").select();
                    }
                    return false;
                });
            widget.find(".popup-button").hide();
            widget.find("span.popup-button").freemixPopupButton("Edit View", function() {
                return view.getPopupContent();
            });

            return widget;
        },
        select: function() {
            var control = this.findWidget();
            $(".view-set>li.view", this.getContainer()).removeClass("ui-state-active")
            .find(".popup-button").hide();

            control.addClass("ui-state-active");
            control.find('.popup-button').show();
            this.display();
        },
        remove: function() {
            var container = this.getContainer();
            this.findWidget().remove();
            var next = container.find(".view-set>li.button:first");
            if (next.size() > 0) {
                next.data("model").select();
            } else {
                container.find(".view-content").empty();
            }
        },
        display: function() {},
        generateExhibitHTML: function(config) {},
        showEditor: function(vc) {
            vc.hidePopup();
            vc.addView(this);
        },
        _setupViewForm: function(config) {
            config = config || this.config;
            var content = this.getContent();

            content.find("form").submit(function() {return false;});

        },
        _setupLabelEditor: function(config) {
            config = config||this.config;
            var view = this;
            var label = this.getContent().find("#view_label_input");

            label.val(config.name);
            label.change(function() {
                view.rename($(this).val());
            });
        },
        _setupTitlePropertyEditor: function(config) {
            //TODO

        }

     });

    Freemix.view = {
        types: [],
        addViewType: function(content) {
            var type = content.config.type;
            Freemix.view.types.push(type);

            var proto = $.extend(true, {},Freemix.exhibit.view,content);
            if (content.propertyTypes) {
                proto.propertyTypes = content.propertyTypes;
            }
            Freemix.view.prototypes[type]=proto;
        },
        prototypes: {},
        createView: function(properties) {
             var props = $.extend({}, properties);
             if (!props.id) {
                 props.id = $.make_uuid();
             }
             return $.extend(true, {}, Freemix.view.prototypes[props.type], {"config": props});

         },
        getViewContainer: function(id) {
            return $(".view-container#" + id, Freemix.getBuilder()).data("model");
        }
     };
})(window.Freemix.jQuery, window.Freemix);
