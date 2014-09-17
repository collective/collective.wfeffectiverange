$(document).ready(function () {

//    wenn effective.changed dann vocab neuladen und options von expires
//    nachladen mit json schnipsel


    function reload_vocab() {
//        replace each option, except the first one
        $("#form-widgets-IPubexBehavior-exp_transition option").slice(1).each(function(){
            // add $(this).val() to your list
//            da no von da view die daten hohlen
            alert($(this).val())
        });

    };

    $( "#form-widgets-IPubexBehavior-eff_transition" ).change(function() {
//        alert('blub');
        reload_vocab();
    });

});

