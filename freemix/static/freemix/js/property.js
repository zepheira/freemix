/*global jQuery */
(function($, Freemix) {

    function mergeProperties(pl, propertyList) {
        $.each(propertyList, function() {
            var name = this.property;
            if (!pl[name]) {
                pl[name] = Freemix.property.createProperty(this);
            }
        });
    }

    var context;
    Freemix.property = {
        add: function(config) {
            Freemix.profile.properties.push(config);
            var prop = this.createProperty(config);
            this.propertyList[config.property] = prop;
            return prop;
        },
        createProperty: function(config) {
            return $.extend(true, {}, Freemix.property.prototype, {
                config: config
            });
        },
        prototype: {
            config: {property: '', enabled: true, tags: [], width: undefined},
            name: function() {
                return this.config.property;
            },
            enabled: function(enabled) {
                if (enabled !== undefined) {
                    this.config.enabled = enabled;
                }
                return this.config.enabled;
            },
            label: function(label) {
                if (label !== undefined) {
                    this.config.label = label;
                }
                return this.config.label || this.config.property;
            },
            hasType: function(type) {
                return this.type() == type;
            },
            expression: function() {
                return "." + this.config.property;
            },
            type: function(type) {
                if (type) {
                    var tags = ["property:type=" + type];
                    this.config.tags = tags;
                    return type;
                }
                if (this.config.tags.length > 0) {
                    return this.config.tags[0].substring(14);
                }
                return "text";
            },

            getExhibitHtml: function() {
                return "<span ex:content='" + this.expression() + "'/>";
            },
            getValueHtml: function(value) {

                if (!context) {
                   context = new Exhibit.UIContext();
                }


//
                var valfun = Freemix.property.type[this.type()].getValueHtml;
                var p = this;
                var response;
                if (value.length === 0) {

                    response =  $("<em>No Value</em>");

                } else if (value.length > 1) {
                    var set = new Exhibit.Set(value);
                    context.formatList(set, set.size(), this.type(), function(n) {
                        response = $(n);
                    });
                } else {
                    context.format(value, this.type(), function(n) {
                        response = $(n);
                    });
                }

                return response;
            },
            remove: function() {
                property = this;
                delete Freemix.property.propertyList[this.config.property];
                var indexes = [];
                $.each(Freemix.profile.properties, function(inx, p) {
                   if (p.property === property.config.property) {
                        indexes.push(inx);
                   }
                });
                if (indexes.length > 0) {
                    indexes.sort(function(a,b) { return b-a; });
                    $.each(indexes, function(inx, index) {
                        Freemix.profile.properties.splice(index, 1);
                    });
                }

            }
        },
        initializeDataProfile: function() {
            var pl = {};
            mergeProperties(pl, Freemix.profile.properties);

            var props = [];
            $.each(pl, function() {
                props.push(this.config);
            });
            Freemix.profile.properties = props;
            this.propertyList = pl;
        },
        initializeFreemix: function() {
            var pl = {};

            var localProperties = Freemix.data_profile.properties;
            mergeProperties(pl, Freemix.data_profile.properties);

            var props = [];
            Freemix.profile.localProperties = {};
            $.each(pl, function() {
                var p = this.config;
                props.push(p);
                $.each(localProperties, function() {
                    if (p.property === this.property) {
                        Freemix.profile.localProperties[p.property] = p;
                    }
                });
            });
            this.propertyList = pl;
        },
        propertyHasType: function(property, type) {
            return (typeof this.propertyList[property] !== "undefined" && this.propertyList[property].hasType(type));
        },
        getPropertiesWithType: function(type) {
            var results = [];
            $.each(this.propertyList, function(name, prop) {
                if (prop.hasType(type) && prop.enabled()) {
                    results.push(prop);
                }
            });
            return results;
        },
        getPropertiesWithTypes: function(types) {
            var results = [];
            $.each(this.propertyList, function(name, prop) {
                if (prop.enabled()) {
                    var found = false;
                    $.each(types, function() {
                        if (prop.hasType(this)) {
                            found = true;
                        }
                    });
                    if (found) results.push(prop);
                }
            });
            return results;
        },
        enabledProperties: function() {
            var results = {};
            $.each(this.propertyList, function(name, prop) {
                if (prop.enabled()) {
                    results[name] = prop;
                }
            });
            return results;
        },

        type: {}
    };

    Freemix.property.type.text = {

        getExhibitHtml: function(metadata) {
           return "<span ex:content='" + metadata.expression() + "'/>";
        }
    };

    Freemix.property.type.url = {
        label: "URL"

//        getExhibitHtml: function(metadata) {
//            return "<a ex:href-content='" +  metadata.expression() + "' target='_blank'><span ex:content='" +  metadata.expression() + "'></span></a>";
//        }
    };

    Freemix.property.type.image = {

//        getExhibitHtml: function(metadata) {
//            return "<a class=\"dialog-thumb lightbox\" ex:href-content='" + metadata.expression() + "'><img ex:src-content='" + metadata.expression() + "'/></a>";
//        }
    } ;


    Freemix.property.type.date = $.extend({}, Freemix.property.type.text,{
        label: "date/time"
    });
    Freemix.property.type.location = $.extend({}, Freemix.property.type.text, {

    });

    Freemix.property.type.number = $.extend({}, Freemix.property.type.text, {

    });

})(window.Freemix.jQuery, window.Freemix);
