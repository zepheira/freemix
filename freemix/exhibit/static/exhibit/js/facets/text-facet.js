/*global jQuery */

(function($, Freemix) {

     $.fn.textFacetEditor = function(facet, okHandler) {
         return this.each(function() {
             if (facet) {
                $(this).data("model", facet);
                if (okHandler) {
                    $(this).data("okhandler", okHandler);
                } else {
                    $(this).removeData("okhandler");
                }
                $(this).find("textarea").val(facet.config.text || "");
                $("#text-facet-preview").empty().creole(facet.config.text || "");
                $(this).dialog("open").find("textarea").focus();
             } else {
                 $(this).dialog({
                     autoOpen: false,
                     width: '80%',
                     modal: true,
                     draggable: false,
                     resizable: false,
                     title: "Edit Text Facet",
                     buttons: {
                         "Ok": function() {
                             var model = $(this).data("model");
                             model.config.text = $(this).find("textarea").val();
                             model.findWidget().find(".facet-content").empty().append(model.generateContent());

                             $(this).dialog("close");
                             okHandler = $(this).data("okhandler");
                             if (okHandler) {
                                 okHandler(model);
                             }
                         },
                         "Cancel": function() {
                             $(this).dialog("close");
                         }
                     }
                 });
                 $("#text-facet-editor textarea").keyup(function() {
                     $("#text-facet-preview").empty().creole($(this).val());
                 });
             }
         });
     };
     var creole = new Parse.Simple.Creole({
         forIE: document.all,
         interwiki: {

         },
         linkFormat: ''
       });
     $.fn.creole = function(text) {

         return this.each(function() {
             if (text) {
                 creole.parse($(this).get(0), text);
            }
         });


     };

     Freemix.facet.addFacetType({
        thumbnail: "/static/exhibit/img/logo-facet.png",
        label: "Text",
        config: {
            type: "text",
            text: undefined
        },
        generateExhibitHTML: function() {
            var text = $("<div class='text-facet'>").creole(this.config.text);
            return text;
        },
        generateContent: function() {
            var facet = this;
            result = $("<div><a href='#'>Edit</a><hr><div class='text-facet-content'></div></div>");
            $("a", result).click(function() {
                $("#text-facet-editor").textFacetEditor(facet);
                return false;
            });
            $(".text-facet-content", result).append(this.generateExhibitHTML());
            return result;
        },
        showEditor: function(facetContainer) {
            facetContainer.hidePopup();
            $("#text-facet-editor").textFacetEditor(this, function(facet) {
                facetContainer.addFacet(facet);
            });
        }

    });


    $(document).ready(function() {
        $("#text-facet-editor").textFacetEditor();
    });


})(window.Freemix.jQuery, window.Freemix);
