/*global jQuery */
(function($, Freemix) {
    Freemix.mapViewLib = {};

    // Display the view's UI.
    Freemix.mapViewLib.display = function(o) {
        var content = o.getContent();
        root = Freemix.getTemplate("map-view-template");
        content.empty();
        root.appendTo(content);
        o.findWidget().recordPager(
            function(row, model, metadata) {
                $("<td class='inner'></td>").insertAfter(row.find("td.visible")).createChildCheck({
                    radio: true,
                    checked: model.config.colorKey === metadata.property,
                    change: function() {
                        if ($(this).is(":checked")) {
                            model.config.colorKey = metadata.property;
                        }
                    },
                    name: 'colorKey'
                });

                if (Freemix.property.propertyHasType(metadata.property, "location")) {
                    $("<td class='inner'></td>").insertAfter(row.find("td.visible")).createChildCheck({
                        radio: true,
                        checked: model.config.latlng === metadata.property,
                        change: function() {
                            if ($(this).is(":checked")) {
                                model.config.latlng = metadata.property;
                            }
                        },
                        name: 'latlng'
                    });
                } else {
                     $('<td class="inner"><input type="radio" disabled="true" /></td>').insertAfter(row.find("td.visible"));
                }

                if (Freemix.property.propertyHasType(metadata.property, "url")) {
                    $("<td class='inner title-link-option'></td>").insertAfter(row.find("td.visible")).createChildCheck({
                        radio: true,
                        checked: model.config.titleLink === metadata.property,
                        change: function() {
                            if ($(this).is(":checked")) {
                                model.config.titleLink = metadata.property;
                            }
                        },
                        name: 'titleLink'
                    });
                } else {
                    $('<td class="inner title-link-option"><input type="radio" disabled="true" /></td>').insertAfter(row.find("td.visible"));
                }

                $("<td class='inner'></td>").insertAfter(row.find("td.visible")).createChildCheck({
                    radio: true,
                    checked: model.config.title === metadata.property,
                    change: function() {
                        if ($(this).is(":checked")) {
                            model.config.title = metadata.property;
                            $('.view-content:visible .title-link-option').fadeIn();
                        }
                    },
                    name: 'title'
                });
            }
        );
        $('#clear-color').bind('click', function() {
            o.config.colorKey = null;
        });
        $('#clear-title').bind('click', function() {
            o.config.title = null;
            $('.view-content:visible .title-link-option').fadeOut();
        });
        $('#clear-title-link').bind('click', function() {
            o.config.titleLink = null;
        });
        if (typeof o.config.title !== "undefined" && o.config.title != null) {
            $('.view-content:visible .title-link-option').show();
        }
        if (typeof o.config.latlng === "undefined") {
            $('.required-setting').show();
            $('.required-setting:visible').bind('mouseover', function() {
                $('#'+$(this).attr('rel')).addClass('ui-state-highlight');
            }).bind('mouseout', function() {
                $('#'+$(this).attr('rel')).removeClass('ui-state-highlight');
            });
            $('input[name=latlng]').bind('change', function() {
                $('.required-setting:visible').hide();
            });
        } else {
            $('.required-setting:visible').hide();
        }
    };

    Freemix.mapViewLib.generateExhibitHTML = function(o, viewClass) {
        if (!o.config.latlng) {
            return $("<div ex:role='view' ex:viewClass='"+viewClass+"' ex:viewLabel='Location Missing'></div>");
        }
        var latlng = o.config.latlng;
        var colorKey = o.config.colorKey;
        var view = $("<div ex:role='view' ex:viewClass='"+viewClass+"' ex:viewLabel='" + o.config.name + "'></div>");
        if (latlng) {
            view.attr("ex:latlng", '.' + latlng);
        }
        if (colorKey) {
            view.attr("ex:colorKey", '.' + colorKey);
        }

        var lens = $("<div class='map-lens' ex:role='lens' style='display:none'></div>");
        var props = Freemix.property.enabledProperties();

        var title = $("<div class='exhibit-title ui-widget-header'></div>");
        if (o.config.title) {
            var html = "<span ex:content='" + props[o.config.title].expression() + "' ></span>";
            if (o.config.titleLink) {
                html += "&nbsp;<a ex:href-content='" + props[o.config.titleLink].expression() + "' target='_blank'>(link)</a>";
            }
            title.append(html);
        }

        var table = $("<table class='property-list-table exhibit-list-table'></table>");
        $.each(o.config.metadata,
        function(index, metadata) {
            var property = metadata.property;
            var identify = props[property];
            if (!metadata.hidden && identify) {
                var label = identify.label();
                $("<tr class='exhibit-property'><td class='exhibit-label'>" + label + "</td><td class='exhibit-value'>" + Freemix.exhibit.renderProperty(metadata) + "</td></tr>").appendTo(table);
            }

        });
        lens.append(table).appendTo(view);
        return view;
    };

})(window.Freemix.jQuery, window.Freemix);
