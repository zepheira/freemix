/*global jQuery */
(function($, Freemix) {

    var identify;

    function setupIdentifier(data) {
        if (!Freemix.profile) {
            Freemix.profile = data.data_profile;
        }
        Freemix.property.initializeDataProfile();

        var db = $.exhibit.initializeDatabase(data, function() {});

        identify = new Freemix.Identify(db);
        $(".editable").each(function() {
            var $this = $(this);

            var placeholder = $("#title-placeholder").text();

            $this.editable(function(value,settings) {
                Freemix.profile.label = (value === placeholder) ? undefined : value;
                return value;
            }, {
                onblur: function(value, settings) {
                    $('form', $this).submit();
                },
                placeholder:placeholder,
                tooltip: placeholder,
                width: '98%'
            });
            if (Freemix.profile.label) {
                $this.text(Freemix.profile.label);
            }
        });
        if (db.getAllItemsCount()<=1) {
            $("button.data-record-delete").hide();
        }
        $("#contents").show();
        $("#contents").data("identifier", identify);

        $("#contents").trigger("post_setup_identifier.dataset", data);

        return identify;
    }
    var publishing = false;
    function publish() {
        if (!publishing) {
            $("#publish").trigger("pre_publish.dataset");
            var metadata = Freemix.profile;
            $('#publish-label input').blur();
            if (!Freemix.profile.label || Freemix.profile.label.length === 0) {
                $("#publish>div").hide();
                $("#publish-name").val("");
                $("#publish-label").show();
            } else {
                publishing=true;
                metadata = $.extend({},  $.exhibit.exportDatabase($.exhibit.database), {"data_profile": metadata});
                if (window.location.hash.startsWith("#dataset=")) {
                    var publishURL = window.location.hash.substring("#dataset=".length, window.location.hash.length);
                } else{
                    publishURL = $("link[rel='freemix/publish']").attr("href");
                }

                var xhr = $.ajax({
                 url: publishURL,
                 type: "PUT",
                 data: $.toJSON(metadata),
                 success: function(data) {
                    $("#publish>div").hide();
                    var url = $(String(data)).find("a").attr("href");
                    // IE7 behaves differently here; need to strip
                    // protocol and host from url, which it seems to
                    // prepend just because.
                    if (url.indexOf('http://') >= 0) {
                        url = url.substr(7);
                        url = url.substr(url.indexOf('/'));
                    }
                    if ($("link[rel='freemix/publish']").attr("href") != url) {
                        window.location.hash = "dataset=" + url;
                        $("link[rel='freemix/publish']").attr("href", url);
                        Freemix.profile.url=url+"data.json";
                    }
                    $("#publish #publish-url").empty().append(data);


                    var freemix_url = $("#publish-success .hyper-upload a.build-freemix").attr("href");
                    if (freemix_url.indexOf("&dataset=") < 0) {
                        $("#publish-success .hyper-upload a.build-freemix").attr("href", freemix_url+"&dataset=" + Freemix.profile.url);
                    }

                    $(".step-menu a span.initial").hide();
                    $(".step-menu span.success").show();
                    publishing = false;
                    $("#publish").trigger("publish_success.dataset");
                    $("#publish").trigger("post_publish.dataset");
                    $("#publish-success").show();
                 },
                 error: function (r, textStatus, error) {
                     $("#publish>div").hide();
                     $("#publish-failed #publish-error").empty().append(textStatus + " " + error);
                     publishing = false;
                     $("#publish").trigger("publish_fail.dataset");
                     $("#publish").trigger("post_publish.dataset");
                     $("#publish-failed").show();
                 }
                });
            }
        }
        return false;
    }

    function deleteRecord() {
        var index = identify.getCurrentRecord();
        var id = $.exhibit.database.getAllItems().toArray()[index];
        $.exhibit.database.removeItem(id);

        if ($.exhibit.database.getAllItemsCount() <= 1) {
            $("button.data-record-delete").hide();
        }

        identify.setCurrentRecord(identify.getCurrentRecord());
        identify.populateRecordDisplay();
    }

     Freemix.DatasetEditor = function() {

        $("#profile-name-button").click(function() {
            Freemix.profile.label = $("#profile-name").val();
            $(".editable#profile-label").text(Freemix.profile.label);
            publish();
        });

        $("#delete-record-dialog").dialog({
            resizable: false,
            height:"auto",
            modal: true,
            autoOpen: false,
            position: 'center',
            buttons: {
                'Delete': function() {
                    deleteRecord();
                    $(this).dialog('close');
                },
                Cancel: function() {
                        $(this).dialog('close');
                }
            }
        });

        $("button.data-record-delete").button({
            "icons": {"primary": "ui-icon-trash"}
        }).click(function(e) {
            $("#delete-record-dialog").dialog("open");
            return false;
        });

    };

    Freemix.DatasetEditor.prototype = {
        setData: function(data) {
            setupIdentifier(data);
        }

    };

    Freemix.Identify.prototype._addPropertyForProfileEditor = Freemix.Identify.prototype.addProperty;
    Freemix.Identify.prototype.addProperty = function(property) {
        var row = this._addPropertyForProfileEditor(property);
        var d = $("<td class='delete'></td>").appendTo(row);
        if (!(property.name() == "label" || property.name() == "id")) {
            $("<a href='' class='button_link negative-button delete_property'>X</a>").click(function(e) {
                $("#delete-property-dialog").data("property", property);
                $("#delete-property-dialog").dialog("open");
                e.preventDefault();
            }).appendTo(d).wrap('<p class="delete-property-wrap"></p>');
        }
        return row;

    };

    $(document).ready(function() {
        $("#delete-property-dialog").dialog({
            resizable: false,
            height:"auto",
            modal: true,
            autoOpen: false,
            position: 'center',
            buttons: {
                'Delete': function() {
                    var property = $("#delete-property-dialog").data("property");
                    property.remove();
                    var db = identify.database;
                    db.getAllItems().visit(function(id) {
                        db.removeObjects(id, property.name());
                    });

                    $("button.data-refresh").trigger("update");
                    identify.populateRecordDisplay();
                    $(".property-row#" + property.config.property).fadeOut().detach();
                    $(this).dialog('close');
                },
                Cancel: function() {
                        $(this).dialog('close');
                }
            }
        });

        var profileURL = $("link[rel='freemix/dataprofile']").attr("href");

        var xhr = $.ajax({
                 url: profileURL,
                 type: "GET",
                 dataType: "json",
                 success: function(data) {
                     var editor = new Freemix.DatasetEditor();
                     editor.setData(data);
                     
                 }
        });
    });

})(jQuery, jQuery.freemix);
