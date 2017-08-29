$(document).ready(function() {

    function basic_parameters (start_node) {
        var $start_node = $(start_node);
        var wftype = $start_node.closest('section').data('wftype');
        var actionurl = $start_node.closest('section').data('actionurl');
        var uuid = $start_node.closest('tr').data('uuid');
        return {
            wftype: wftype,
            actionurl: actionurl,
            uuid: uuid
        };
    }

    // Remove the URL parameters
    history.replaceState({} , '', window.location.href.split('?')[0]);

    $('select[name="transition"]').on('change', function(e) {
        var val = this.value || undefined;
        var basic = basic_parameters(this);

        window.location.href = basic.actionurl
            + '&wfype=' + basic.wftype
            + '&transition=' + val
            + '&uuid=' + basic.uuid;
    });

    $('input[name="transition_date"]').on('updated.pickadate.patterns', function(e) {
        var val = this.value || undefined;
        var basic = basic_parameters(this);

        window.location.href = basic.actionurl
            + '&wfype=' + basic.wftype
            + '&transition_date=' + val
            + '&uuid=' + basic.uuid;
    });

});
