/*global jQuery */

 (function($, Freemix) {

     Freemix.facet.addFacetType({
         thumbnail: "/static/exhibit/img/logo-facet.png",
         label: "Logo",
         config: {
            type: "logo",
            src: undefined,
            alt: undefined,
            href: undefined,
            width: undefined,
            height: undefined
        },
        generateExhibitHTML: function() {
            var img = $("<img/>");
            if (this.config.src) {
                img.attr("src", this.config.src);
            }
            if (this.config.alt) {
                img.attr("alt", this.config.alt);
            }
            if (this.config.width) {
                img.attr("style", "max-width:" + this.config.width + "px");
            }
            if (this.config.href) {
                var link = $("<a/>");
                link.attr("href", this.config.href);
                link.append(img);
                var p = $("<span/>");
                p.append(link);
                return p.html();
            }
            var s = $("<span/>");
            s.append(img);
            p = $("<span/>");
            p.append(s);
            return p.html();
        },
        showEditor: function(facetContainer) {
            var view = this;
            var config = view.config;
            var editor = Freemix.getTemplate("logo-facet-editor");

            editor.find("form").submit(function() {
                var e = facetContainer.popupApi().elements.content;
                e.find(".error").removeClass("error");
                e.find(".errorField").hide();
                if (config.src && config.src.length > 0) {
                    facetContainer.hidePopup();
                    facetContainer.addFacet(view);
                } else {
                    e.find("#div_id_src").addClass("error");
                    e.find("#div_id_src .errorField").show();
                }
                return false;
            });


            $("#id_src", editor).change(function(event) {
                config.src = $(event.target).val();
            });
            $("#id_alt", editor).change(function(event) {
                config.alt = $(event.target).val();
            });
            $("#id_href", editor).change(function(event) {
                config.href = $(event.target).val();
            });
            $("#cancel-button", editor).click(function(event) {
                facetContainer.hidePopup();
                return false;
            });
            facetContainer.setPopupContent(editor);

        },
        generateContent: function() {
            var config = this.config;
            var html = $(this.generateExhibitHTML());
            var img = html.find("img");
            if (config.width) {
                img.attr("style", "max-width:" + config.width + "px");
            }
            var slider = $("<div/>");
            slider.slider({
                slide: function(event, ui) {
                    config.width = ui.value;
                    img.attr("style", "max-width:" + config.width + "px");
                    return true;
                }
            });
            img.load(function() {
                var naturalWidth = img.get(0).naturalWidth;
                if (!naturalWidth) {
                    naturalWidth = img.get(0).width * 2;
                }
                slider.slider('option', 'max', naturalWidth);
                slider.slider('option', 'value', img.get(0).width);
            });
            var div = $("<div/>");
            var block = $("<div/>");
            block.append(img);
            div.append(slider);
            div.append(block);
            if (config.href) {
                div.append($("<div>Link: <em>" + config.href + "</em></div>"));
            }
            return div;
        }
    });

})(jQuery, jQuery.freemix);
