/*global jQuery */
(function($, Freemix) {


    function setupExhibit(data) {
        var db = $.exhibit.initializeDatabase({"items": data["items"]});
        new $.freemix.Identify(db);
        $("#contents").show();
    }

    function setupProfile(profile) {
        Freemix.profile = profile;
        Freemix.property.initializeDataProfile();
        var dataURL = $("link[rel='exhibit/data']").attr("href");
        $.ajax({
            url: dataURL,
            type: "GET",
            dataType: "json",
            success: function(data) {
                setupExhibit(data);
            }

        })

    }

    function setup() {
         var url = $("#create_exhibit_button").attr("href");
        $("#create_exhibit_button").newExhibitDialog(url);

        var profileURL = $("link[rel='freemix/dataprofile']").attr("href");
        $.ajax({
            url: profileURL,
            type: "GET",
            dataType: "json",
            success: function(data) {
                setupProfile(data);
            }
        });


    }
    $(document).ready(setup);
})(jQuery, jQuery.freemix);