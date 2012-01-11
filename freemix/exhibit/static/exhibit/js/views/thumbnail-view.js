/*global jQuery */
 (function($, Freemix) {

     // Display the view's UI.
     function display() {
         var content = this.getContent();
         var root = Freemix.getTemplate("thumbnail-view-template");

         content.empty();
         content.append(root);
         this._setupViewForm();
         this._setupLabelEditor();

         var images = Freemix.property.getPropertiesWithType("image");

         var image = content.find("#image_property");

         // Set up image property selector
         this._setupSelectOptionHandler(image, "image", images);
         this._setupTitlePropertyEditor();

         image.change();
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
