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
        var dataURL = $("link[rel='freemix/data']").attr("href");
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
        var profileURL = $("link[rel='freemix/profile']").attr("href");
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