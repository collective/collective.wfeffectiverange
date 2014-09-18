$(document).ready(function () {

    function reload_vocab(current) {
//        this function reloads the possible values for exp_transition, each time
//        eff_transition has changed

        // get current options
        var options = $("#form-widgets-IPubexBehavior-exp_transition option");
        //get expires selector
        var selector =  $("#form-widgets-IPubexBehavior-exp_transition");
            // remove old options
            selector.empty();

        $.getJSON("@@wfpubex_vocab?current=" + current, function (result) {
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

    $("#form-widgets-IPubexBehavior-eff_transition").change(function () {
        reload_vocab($(this).val());
    });
});

