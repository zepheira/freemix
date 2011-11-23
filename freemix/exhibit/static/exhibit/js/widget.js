(function($, Freemix) {

    Freemix.exhibit = Freemix.exhibit || {};
    Freemix.exhibit.container = {
        id: "",
        getPopupButton: function() {
            return this.findWidget().find(".popup-button");
        },
        setPopupContent: function(content) {
            var api = this.popupApi();
            api.updateContent("<div style='display:none;'></div>");
            api.updateContent(content);
        },
        popupApi: function() {
            return this.getPopupButton().qtip("api");
        },
        hidePopup: function() {
            this.getPopupButton().qtip("hide");
        }
    };


    Freemix.exhibit.widget = {
        config: {
            id: "",
            name: ""
        },
        findWidget: function() {
            if (!this._selector) {
                this._selector = this.generateWidget();
            }
            return this._selector;
        },
        getConfig: function() {
            return this.config;
        },
        generateWidget: function() {
            return $("<div>");
        },
        remove: function() {
            this.findWidget().remove();
        },
        rename: function(name) {
            this.config.name = name;
            this.findWidget().find("span.label").text(name);
        },
        hidePopup: function() {
            this.findWidget().find(".popup-button").qtip("hide");
        },
        setPopupContent: function(content) {
            var api = this.popupApi();
            api.updateContent("<div style='display:none;'></div>");
            api.updateContent(content);
        },
        popupApi: function() {
            return this.findWidget().find(".popup-button").qtip("api");
        },
        getPopupContent: function() {
            var w = this;
            return $("<span><a href='#' class='rename'>Rename</a> | <a href='#' class='delete'>Delete</a></span>").find(".rename").click(function() {
                var dialog = $("<span><input type='text' value='" + w.config.name +
                    "' id='rename-component' /><div class='rename-component-buttons'>" +
                    "<span class='button ui-state-default ui-corner-all'>OK</span>" +
                    "<span class='button ui-state-default ui-corner-all'>Cancel</span></div></span>");
                dialog.keydown(function(e) {
                    var code = (e.keyCode ? e.keyCode: e.which);
                    if (code == $.ui.keyCode.ENTER) {
                        var value = $('input#rename-component', w.popupApi().elements.content).val();
                        w.rename(value);
                        w.hidePopup();
                    } else if (code == $.ui.keyCode.ESCAPE) {
                        w.hidePopup();
                    }
                });
                dialog.find('span.button:eq(0)').bind('click',function() {
                    var value = $('input#rename-component', w.popupApi().elements.content).val();
                    w.rename(value);
                    w.hidePopup();
                });
                dialog.find('span.button:eq(1)').bind('click',function() {
                    w.hidePopup();
                });
                w.setPopupContent(dialog);
                w.popupApi().elements.content.find("input#rename-component").focus();
                return false;
            }).end().find(".delete").click(function() {
                w.hidePopup();
                w.remove();
            }).end();
        },
        propertyTypes: ["text", "image", "currency", "url", "location", "date", "number"],

        isAvailable: function() {
            return Freemix.property.getPropertiesWithTypes(this.propertyTypes).length > 0;
        }
    };

    Freemix.exhibit.renderProperty = function(metadata) {
        var property = Freemix.property.propertyList[metadata.property];
        if (property.enabled()) {
            return property.getExhibitHtml();
        } else {
            return "";
        }
    };


    $.fn.createChildCheck = function(config) {
        return this.each(function() {
            var $this = $(this);
            var type = 'checkbox';

            if (config.name) {
                name = config.name;
            } else {
                name = $.make_uuid();
            }
            if (config.radio) {
                type = 'radio';

            }
            disabled = "";
            if (config.enabled) {
                if (!config.enabled()) {
                    disabled = " disabled='true'";
                }
            }
            var check = $("<input type='" + type + "' name='" + name + "'" + disabled + "/>");
            $this.append(check);
            if (config.checked) {
                check.attr("checked", "checked");
            }
            if (config.change) {
                check.click(config.change);
            }
        });
    };
})(window.Freemix.jQuery, window.Freemix);
