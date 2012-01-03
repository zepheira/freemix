/*global jQuery */
 (function($, Freemix) {

     function createSelectOptionHandler(model) {
         return function(selector, key, collection, nullable) {

             if (nullable) {
                 selector.append("<option value=''></option>");
             }
             $.each(collection, function() {
                 var option = "<option value='" + this.name() + "'>" + this.label() + "</option>";
                 selector.append(option);
             });

              selector.change(function() {
                   var value = $(this).val();
                   if (value && value != ( "" || undefined)) {
                       model.config[key] = value;
                   } else {
                       model.config[key] = undefined;
                   }
               }).val(model.config[key]);

              if (!selector.val()) {
                 selector.get(0).options[0].selected = true;

              }

           };
     }


     // Display the view's UI.
     function display() {
         var view = this;
         var config = this.config;
         var content = this.getContent();
         var root = Freemix.getTemplate("thumbnail-view-template");

         content.empty();
         content.append(root);
         content.find("form").submit(function() {return false;});
         this._setupViewForm();
         this._setupLabelEditor();

         var setupHandler = createSelectOptionHandler(this);
         var images = Freemix.property.getPropertiesWithType("image");
         var links = Freemix.property.getPropertiesWithTypes(["image", "url"]);
         var titles = Freemix.property.enabledProperties();

         var image = content.find("#image_property");
         var title = content.find("#title_property");
         var title_link = content.find("#title_link_property");


         // Set up image property selector
         setupHandler(image, "image", images);
         setupHandler(title, "title", titles, true);
         title.change(function() {
             if (title.val() && links.length > 0) {
                 title_link.removeAttr("disabled");
             } else {
                 title_link.attr("disabled", true);
                 title_link.val("");
             }
         });
         title.change();

         if (links.length > 0) {
             setupHandler(title_link, "titleLink", links, true);
         } else {
             title_link.attr("disabled", true);
         }
         image.change();
         title.change();
         title_link.change();


     }

    function generateExhibitHTML(config) {
        config = config || this.config;
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
            abbreviatedCount: "12"
        }
    });

})(window.Freemix.jQuery, window.Freemix);
