/*global jQuery */
(function($, Freemix) {
   var data = {{ json|safe }};

   if (data["data_profile"]) {
       Freemix.profile=data["data_profile"];
   }
   if (data["items"]) {
       Freemix.data = {"items": data["items"]};
   }
})(jQuery, jQuery.freemix);
