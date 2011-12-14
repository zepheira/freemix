/*global jQuery */
 (function($, Freemix) {

      // Display the view's UI.
     function display() {
         var content = this.getContent();
         var root = Freemix.getTemplate("table-view-template");
         content.empty();
         root.appendTo(content);

         this.findWidget().recordPager(
             function(row, model, metadata) {
                 $("<td class='inner'></td>").insertAfter(row.find("td.visible")).createChildCheck({
                     radio: true,
                     checked: model.config['sortProperty'] === metadata.property,
                     change: function() {
                         if ($(this).is(":checked")) {
                             model.config['sortProperty'] = metadata.property;
                         }
                     },
                     name: 'sortProperty'
                 });
                 row.find('td.visible input:checkbox', content).bind('change', function(e) {
                     var t = $(this);
                     if (row.find('td.inner input:radio').is(':checked')) {
                         t.attr('checked', true);
                         metadata.hidden = undefined;
                     } else {
                         row.find('td.inner input:radio').attr('disabled', !t.is(':checked'));
                     }
                 });
                 if (!row.find('td.visible input:checkbox').is(':checked')) {
                     row.find('input[name="sortProperty"]:radio').attr('disabled', true);
                 }
             }
         );

         var m = this;
         $('select.sort-order', content).val(m.config.asc.toString());
         $('select.sort-order', content).bind('change', function(e) {
             m.config.asc = $(this).val() === 'true';
         });
     }

    function generateExhibitHTML() {
        var config = this.config;
        var empty = true;

        var props = Freemix.property.enabledProperties();
        $.each(config.metadata,
        function(index, metadata) {
            var property = metadata.property;
            var identify = props[property];
            if (!metadata.hidden && identify) {
                empty = false;
            }

        });
        if (empty) {
            return $("<div ex:role='view' ex:viewLabel='Columns Missing'></div>");
        }
        var view = $("<div ex:role='view' ex:viewClass='Tabular' ex:viewLabel='" + this.config.name + "'></div>");
        var labels = [];
        var columns = [];
        $.each(config.metadata,
        function(index, metadata) {
            var property = metadata.property;
            var identify = props[property];
            if (!metadata.hidden && identify) {
                labels[labels.length] = identify.label();
                columns[columns.length] = identify.expression();
            }

        });
        view.attr("ex:columnLabels", labels.join(', '));
        view.attr("ex:columns", columns.join(', '));
        if (config.sortProperty) {
            var indexOffset = 0;
            $.each(config.metadata,
            function(index, metadata) {
                var property = metadata.property;
                if (config.sortProperty === property) {
                    view.attr("ex:sortColumn", index - indexOffset);
                }
                if (metadata.hidden) indexOffset++;
            });
        }
        view.attr("ex:sortAscending", config.asc);
        return view;
    }

    Freemix.view.addViewType({
        label: "Table",
        thumbnail: "/static/exhibit/img/table-icon.png",
        display: display,
        generateExhibitHTML: generateExhibitHTML,

        config: {
            type: "table",
            sortProperty: undefined,
            asc: true,
            metadata: []
        }
    });

})(window.Freemix.jQuery, window.Freemix);
