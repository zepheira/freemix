/*global jQuery */
(function($, Freemix) {
    var load_timeout=30000;

    function DataLoadTransaction() {}
    DataLoadTransaction.prototype = {
        start : function(xhr) {
            this.id=$.make_uuid();
            this.status = "running";
            window.onbeforeunload = function(e) {
                var msg = "Leaving during upload will cancel the upload process!";
                var evt = e || window.event;
                if (evt) evt.returnValue = msg;
                // for Safari
                return msg;
            };
            if (xhr) {
                this._xhr = xhr;
            }
            this._timeout = setTimeout(function() {
                $("#loading-time-warning").slideDown();

            }, load_timeout);

        },

        _stop: function(status) {
            if (this.status == "running") {
                window.onbeforeunload = null;
                if (this._timeout) {
                    clearTimeout(this._timeout);
                    delete this._timeout;

                }
                this.status = status;
            }
        },

        success : function() {
            this._stop("successful");
            if (this._xhr) {
                delete this._xhr;
            }
        },

        cancel : function() {
            this._stop("cancelled");
            if (this._xhr && this._xhr.abort) {
                this._xhr.abort();
                delete this._xhr;
            }

        },

        failed: function() {
            this._stop("failed");
            if (this._xhr) {
                delete this._xhr;
            }
        },

        validate: function(form) {}
    };

    function FileLoadTransaction() {}
    FileLoadTransaction.prototype = $.extend({}, DataLoadTransaction.prototype, {
        validate: function(form) {
            if (!form.file.value && typeof form.fakefile_file ==="undefined") {
                $("#load-failure-file").fadeIn();
                return false;
            }
            this.data = form.file.value;
            return true;
        },
        source: "file"
    });

    function URLLoadTransaction() {}
    URLLoadTransaction.prototype = $.extend({}, DataLoadTransaction.prototype, {
        validate: function(form) {
            if (!form.url.value) {
                $("#load-failure-url").fadeIn();
                return false;
            }
            switch (form.service.value) {
                case "cdm":
                    if (!form.cdm_collection_name.value && !form.cdm_search_term.value) {
                        $("#load-failure-cdm-no-param").fadeIn();
                        return false;
                    }
                    if (form.cdm_collection_name.value && !form.cdm_collection_name.value.startsWith('/')) {
                        $('#load-failure-cdm-collection').fadeIn();
                        return false;
                    }
                    break;
                case "oai":
                    break;
                default:
                    break;
            }
            this.data = form.url.value;
            return true;
        },
        source: "url"

    });

    $.fn.dataLoadForm = function(tc, use_iframe) {
        return this.each(function() {
            $(this).ajaxForm({
                dataType: "json",
                beforeSubmit: function(formData, jqForm, options) {
                    // Generate a new transaction corresponding to the request type
                    // and start the upload process
                    var transaction = new tc();
                    $("#contents").data("data-load-transaction", transaction);

                    var form = jqForm[0];
                    if (!transaction.validate(form)) {
                        transaction.failed();
                        return false;
                    }

                    $("#load-form, #load-messages>li, #loading-time-warning").hide();
                    transaction.start();
                    $("#loading").fadeIn();
                    return true;
                },
                beforeSend: function(xhr) {
                    // Add the transaction ID to the request header
                    var transaction = $("#contents").data("data-load-transaction");
                    xhr.setRequestHeader("X-Data-Load-TxId", transaction.id);
                    //
                    xhr._tx = transaction;
                    // transaction needs xhr reference for cancel
                    transaction._xhr = xhr;
                    return true;
                },
                success:  function(data, status, xhr, form) {
                    var items = data.items;
                    if (xhr._tx) {
                        var txId = xhr._tx.id;
                    } else {
                        txId = xhr.getResponseHeader("X-Data-Load-TxId");
                    }
                    var currTx = $("#contents").data("data-load-transaction");
                    if (txId == currTx.id && currTx.status == "running") {
                        if (!data.data_profile || !items || items.length === 0) {
                            this.error("");
                        } else {
                            // Set the identifier up only if the transaction ID is current
                            currTx.success();
                            $(".user-profile-menu").fadeOut().empty();
                            setupIdentifier(data);
                        }
                    }
                },
                error: function(xhr, status, error) {
                    var currTx = $("#contents").data("data-load-transaction");
                    if (xhr._tx) {
                        var txId = xhr._tx.id;
                    } else if (!xhr instanceof String) {
                        txId = xhr.getResponseHeader("X-Data-Load-TxId");
                    } else {
                        // Firefox sometimes passes "" for xhr
                        // But the current transaction should be correct, as
                        // cancelling properly kills the request
                        txId = currTx.id;
                    }


                    if (txId == currTx.id && currTx.status == "running") {
                        currTx.failed();
                        $("#loading").hide();
                        $("#load-failure-general, #load-form").fadeIn();
                    }

                },
                iframe: use_iframe===true
            });
        });
    };

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
        $(".step-menu").freemixStepTabs("select", "#identify");

        $("#load #upload-label").hide();
        $("#load #replace-label").show();

        $("#contents").data("identifier", identify);

        $("#contents, #subnav, .step-menu").fadeIn();
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
                if (window.location.hash.startsWith("#data_profile=")) {
                    var publishURL = window.location.hash.substring("#data_profile=".length, window.location.hash.length);
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
                        window.location.hash = "data_profile=" + url;
                        $("link[rel='freemix/publish']").attr("href", url);
                        Freemix.profile.url=url+"data.json";
                    }
                    $("#publish #publish-url").empty().append(data);


                    var freemix_url = $("#publish-success .hyper-upload a.build-freemix").attr("href");
                    if (freemix_url.indexOf("&data_profile=") < 0) {
                        $("#publish-success .hyper-upload a.build-freemix").attr("href", freemix_url+"&data_profile=" + Freemix.profile.url);
                    }
                    $("#publish-success .hyper-upload a.build-freemix").bind("click", function(){
                        $("#create_view_dialog").newViewDialog($("#publish-success .hyper-upload a.build-freemix").attr("href"));
                        return false;
                    });
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

    function resetLoad() {
        $("#loading, ul#load-messages>li").hide();
        $('#upload-from-url *[id^=div_id_cdm_], #upload-from-url *[id^=div_id_oai_]').hide();
        $("#upload-from-file, #upload-from-url").show().find("#div_id_diagnostics,.buttons").hide();
        $("#load-form").fadeIn();
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
        $("#create_view_dialog").newViewDialog();

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

    function showFileForm() {
        $("#load #upload-from-url").fadeOut();
        $("#load #upload-from-file").fadeIn().find("#div_id_diagnostics,.buttons").slideDown();
    }

    function showURLForm() {
        $("#load #upload-from-file").fadeOut();
        $("#load #upload-from-url").fadeIn().find("#div_id_diagnostics,.buttons").slideDown();
    }

    function showCDMDetails() {
        $('#load #upload-from-url *[id^=div_id_cdm_]').slideDown();
    }

    function showOAIDetails() {
        $('#load $upload-from-url *[id^=div_id_oai_]').slideDown();
    }

    function hideCDMDetails() {
        $('#load #upload-from-url *[id^=div_id_cdm_]').hide();
    }

    function hideOAIDetails() {
        $('#load $upload-from-url *[id^=div_id_oai_]').hide();
    }

    Freemix.UploadForm = function() {
        $("#load #upload-from-file form").dataLoadForm(FileLoadTransaction, true);
        $("#load #upload-from-url form").dataLoadForm(URLLoadTransaction);
    };

    Freemix.UploadForm.prototype = {
        show: function() {
            $("#load #upload-label").show();
            $("#load #replace-label").hide();
            $(".step-menu").freemixStepTabs("select", "#load");

            $("#contents").fadeIn();
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
        $(".step-menu").freemixStepTabs({
            publish: publish,
            load: resetLoad
        });

        $("#supported-file-types").dialog({
            autoOpen: false,
            width: 500,
            height: 500,
            modal: true,
            draggable: false,
            resizable: false,
            title: $("#supported-file-types").attr("title")
        });
        $(".supported-file-types").live('click', function(e) {
            e.preventDefault();
            $("#supported-file-types").dialog("open");
        });

        $("#cancel-load-button").live('click', function(e) {
            e.preventDefault();
            var tx = $("#contents").data("data-load-transaction");
            // final sanity check
            if (tx.status != "successful") {
                tx.cancel();
                resetLoad();
            }
        });

        $("#load #upload-from-file #id_file").click(function() {
            showFileForm();
        });

        $("#load #upload-from-url input, #load #upload-from-url select").bind('focus', function() {
            showURLForm();
        });

        $("#upload-from-url, #upload-from-file").find(".negative-button").click(function(e) {
            resetLoad();
        });

        $('#load #upload-from-url #id_service').bind('change', function(e) {
            var service = $(this).val();
            switch (service) {
                case "cdm":
                    showCDMDetails();
                    hideOAIDetails();
                    break;
                case "oai":
                    showOAIDetails();
                    hideCDMDetails();
                    break;
                default:
                    hideCDMDetails();
                    hideOAIDetails();
                    break;
            }
        });

        $(".verify_data_help").click(function(e){
            e.preventDefault();
            $("#load-info-verify-data").slideDown();
        });
    });

})(jQuery, jQuery.freemix);
