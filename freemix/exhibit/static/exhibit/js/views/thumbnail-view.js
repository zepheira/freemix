/*global jQuery */
 (function($, Freemix) {

     function createSetupHandler(model) {
         return function(selector, key, collection, nullable) {
             var content = model.getContent();

             if (nullable) {
                 $(selector, content).append("<option value=''></option>");
             }
             $.each(collection, function() {
                 var option = "<option value='" + this.name() + "'>" + this.label() + "</option>";
                 $(selector, content).append(option);
             });



              model.getContent().find(selector)
               .change(function() {
                   var value = $(this).val();
                   if (value && value != ( "" || undefined)) {
                       model.config[key] = value;
                   } else {
                       model.config[key] = undefined;
                   }
               }).val(model.config[key]);

              if (!$(selector).val()) {
                 $(selector, content).get(0).options[0].selected = true;

              }

           };
     }


     // Display the view's UI.
     function display() {
         var config = this.config;
         var content = this.getContent();
         var root = Freemix.getTemplate("thumbnail-view-template");

         content.empty();
         content.append(root);
         var setupHandler = createSetupHandler(this);
         var images = Freemix.property.getPropertiesWithType("image");
         var links = Freemix.property.getPropertiesWithTypes(["image", "url"]);
         var titles = Freemix.property.enabledProperties();

         // Set up image property selector
         setupHandler("#image_property", "image", images);

         setupHandler("#title_property", "title", titles, true);
         var tp = $("#title_property");
         tp.change(function() {
             if (tp.val() && links.length > 0) {
                 $("#title_link_property", content).removeAttr("disabled");
             } else {
                 $("#title_link_property", content).attr("disabled", true);
                 $("#title_link_property", content).val("");
             }
         });
         tp.change();

         if (links.length > 0) {
             setupHandler("#title_link_property", "titleLink", links, true);
         } else {
             $("#title_link_property", content).attr("disabled", true);
         }
         $("#image_property", content).change();
         $("#title_property", content).change();
         $("#title_link_property", content).change();

     }

    function generateExhibitHTML() {
        var config = this.config;
        var props = Freemix.property.enabledProperties();

        var view = $("<div ex:role='view' ex:viewClass='Thumbnail' ex:viewLabel='" + config.name + "'></div>");
        view.attr("ex:showAll", config.showAll);
        view.attr("ex:abbreviatedCount", config.abbreviatedCount);
        var lens = $("<div ex:role='lens' style='display:none;' class='image-thumbnail ui-state-highlight'></div>");
        var img = $("<a class='lightbox' ex:href-content='." + config.image + "'><img class='image-thumbnail' ex:src-content='." + config.image +"'/></a>");
        lens.append(img);
        if (config.title) {
            var title = $("<div class='name'><span ex:content='." + config.title + "'</div>");
            if (config.titleLink) {
                title.find("span").wrap("<a ex:href-content='." + config.titleLink + "'></a>")
            }
            lens.append(title);
            var formats = "item {title:expression(" + props[config.title].expression() + ")}";
            view.attr("ex:formats", formats);
        }
        view.append(lens);

        return view;
    }

    Freemix.view.addViewType({
        propertyTypes: ["image"],
        label: "Gallery",
        thumbnail: "/static/exhibit/img/gallery.png",
        display: display,
        generateExhibitHTML: generateExhibitHTML,

        config: {
            type: "thumbnail",
            image: undefined,
            title: undefined,
            titleLink: undefined,
            abbreviatedCount: "12",
            metadata: []
        }
    });

})(window.Freemix.jQuery, window.Freemix);
