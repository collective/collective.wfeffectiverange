
$(document).ready(function () {

    function reload_vocab(current, contenttype) {
//        this function reloads the possible values for expires_transition, each time
//        effective_transition has changed

        // get current options
        var options = $("#form-widgets-IPubexBehavior-expires_transition option");
        //get expires selector
        var selector =  $("#form-widgets-IPubexBehavior-expires_transition");
            // remove old options
            selector.empty();

        $.getJSON("@@wfpubex_vocab?current=" + current + "&contenttype=" + contenttype, function (result) {
            //the first option is always 'no-value'
            selector.append(options[0]);

            //set new options
            $.each(result, function (idx, term) {
                var new_option = $("<option></option>")
                new_option.attr("value", term.token).text(term.token);
                selector.append(new_option);
            });
        });
    }

    $("#form-widgets-IPubexBehavior-effective_transition").change(function () {
        //extra geht the portaltype from the url
        var path = window.location.pathname;
        var contenttype = path.replace(/.*\+{2}add\+{2}/, "");
        reload_vocab($(this).val(), contenttype);
    });
});

