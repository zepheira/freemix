/*global jQuery */
 (function($, Freemix) {

     function createSetupHandler(model) {
         return function(selector, key, nullValue) {
              model.getContent().find(selector)
               .change(function() {
                   var value = $(this).val();
                   if (value != (nullValue || "" || undefined)) {
                       model.config[key] = value;
                   } else {
                       model.config[key] = undefined;
                   }
               })
               .val(model.config[key]);
           };
     }



     // Display the view's UI.
     function display() {
         var content = this.getContent();
         var root = Freemix.getTemplate("timeline-view-template");
         content.empty();
         root.appendTo(content);

         var setupHandler = createSetupHandler(this);

         var $start = content.find("#timeline-start-date");
         var $end = content.find("#timeline-end-date");

         setupHandler("#top-band-unit", "topBandUnit");
         setupHandler("#bottom-band-unit", "bottomBandUnit");
         setupHandler("#timeline-start-date", "startDate");
         if (!$("#top-band-unit").val()) {
             $("#top-band-unit").get(0).options[0].selected = true;
             $("#top-band-unit").change();
         }
         if (!$("#bottom-band-unit").val()) {
             $("#bottom-band-unit").get(0).options[0].selected = true;
             $("#bottom-band-unit").change();
         }

         // Read record data into selects.
         $.each(Freemix.property.getPropertiesWithType("date"),
         function() {
             var value = $start.val();
             $start.append('<option value="' + this.name() + '">' + this.label() + '</option>');
             if (!value) {
                 $start.val(this.name());
                 $start.change();
             }
         });

	 $end.append('<option value="">(none)</option>');
         $.each(Freemix.property.getPropertiesWithType("date"),
         function() {
             var value = $end.val();
             $end.append('<option value="' + this.name() + '">' + this.label() + '</option>');
             if (value == this.name()) {
                 $end.val(this.name());
                 $end.change();
             }
         });
         setupHandler("#timeline-end-date", "endDate");

         this.findWidget().recordPager(
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

                 if (Freemix.property.propertyHasType(metadata.property, "date")) {
                     $("<td class='inner'></td>").insertAfter(row.find("td.visible")).createChildCheck({
                         radio: true,
                         checked: model.config.endDate === metadata.property,
                         change: function() {
                             if ($(this).is(":checked")) {
                                 model.config.endDate = metadata.property;
                             }
                         },
                         name: 'endDate'
                     });
                 } else {
                     $('<td class="inner"><input type="radio" disabled="true" /></td>').insertAfter(row.find("td.visible"));
                 }

                 if (Freemix.property.propertyHasType(metadata.property, "date")) {
                     $("<td class='inner'></td>").insertAfter(row.find("td.visible")).createChildCheck({
                         radio: true,
                         checked: model.config.startDate === metadata.property,
                         change: function() {
                             if ($(this).is(":checked")) {
                                 model.config.startDate = metadata.property;
                             }
                         },
                         name: 'startDate'
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
         $('#clear-title').bind('click', function() {
             model.config.title = null;
             $('.view-content:visible .title-link-option').fadeOut();
         });
         $('#clear-title-link').bind('click', function() {
             model.config.titleLink = null;
         });
         $('#clear-end').bind('click', function() {
             model.config.endDate = null;
         });
         $('#clear-color').bind('click', function() {
             model.config.colorKey = null;
         });
         if (typeof this.config.title !== "undefined" && this.config.title != null) {
             $('.view-content:visible .title-link-option').show();
         }
         if (typeof this.config.startDate === "undefined") {
             $('.required-setting').show();
             $('.required-setting:visible').bind('mouseover', function() {
                 $('#'+$(this).attr('rel')).addClass('ui-state-highlight');
             }).bind('mouseout', function() {
                 $('#'+$(this).attr('rel')).removeClass('ui-state-highlight');
             });
             $('input[name=startDate]').bind('change', function() {
                 $('.required-setting:visible').hide();
             });
         } else {
             $('.required-setting:visible').hide();
         }
     }

    function generateExhibitHTML() {
        var config = this.config;
        if (!config.startDate) {
            return $("<div ex:role='view' ex:viewLabel='Range Missing'></div>");
        }
        var props = Freemix.property.enabledProperties();
        var colorKey = config.colorKey;
        var view = $("<div ex:role='view' ex:viewClass='Timeline' ex:viewLabel='" + config.name + "'></div>");
        if (colorKey) {
            view.attr("ex:colorKey", '.' + colorKey);
        }
        if (config.name) {
            view.attr("ex:label", config.name);
        }
        if (config.title) {
            view.attr("ex:eventLabel", "." + config.title);
        }
        if (config.startDate) {
            view.attr("ex:start", "." + config.startDate);
        }
        if (config.endDate) {
            view.attr("ex:end", "." + config.endDate);
        }
        if (config.topBandUnit) {
            view.attr("ex:topBandUnit", config.topBandUnit);
        }
        if (config.bottomBandUnit) {
            view.attr("ex:bottomBandUnit", config.bottomBandUnit);
        }
        if (config.topBandUnitsPerPixel) {
            view.attr("ex:topBandUnitsPerPixel", "." + config.topBandUnitsPerPixel);
        }
        if (config.bottomBandUnitsPerPixel) {
            view.attr("ex:bottomBandUnitsPerPixel", "." + config.bottomBandUnitsPerPixel);
        }

        var lens = $("<div class='timeline-lens ui-widget-content' ex:role='lens' style='display:none'></div>");
        var title = $("<div class='exhibit-title ui-widget-header'></div>");
        if (this.config.title) {
            var html = "<span ex:content='" + props[this.config.title].expression() + "' ></span>";
            if (this.config.titleLink) {
                html += "&nbsp;<a ex:href-content='" + props[this.config.titleLink].expression() + "' target='_blank'>(link)</a>";
            }
            title.append(html);
        }
        lens.append(title);
        var table = $("<table class='property-list-table exhibit-list-table'></table>");
        $.each(this.config.metadata,
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
    }

    Freemix.view.addViewType({
        propertyTypes: ["date"],
        label: "Timeline",
        thumbnail: "/static/exhibit/img/timeline-icon.png",
        display: display,
        generateExhibitHTML: generateExhibitHTML,

        config: {
            type: "timeline",
            title: undefined,
            titleLink: undefined,
            colorKey: undefined,
            startDate: undefined,
            endDate: undefined,
            topBandUnit: undefined,
            topBandPixelsPerUnit: undefined,
            bottomBandUnit: undefined,
            bottomBandPixelsPerUnit: undefined,
            metadata: []
        }
    });

})(window.Freemix.jQuery, window.Freemix);
