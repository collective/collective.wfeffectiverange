$(document).ready(function() {

  function reload_vocab(element) {
    //        this function reloads the possible values for expires_transition, each time
    //        effective_transition has changed

    //extra get the portaltype from the url
    var path = window.location.pathname;
    //        var contenttype = path.replace(/.*\+{2}add\+{2}/, "");

    if (window.location.href.indexOf('addtranslation') > -1) {
      var regex_portal_type = /.*\+{2}addtranslation\+{2}(.*)($|\/.*)/;
      var regex_base_url = /(.*)\/(edit.*|\+{2}addtranslation\+{2}.*)/;

    } else {
      var regex_portal_type = /.*\+{2}add\+{2}(.*)($|\/.*)/;
      var regex_base_url = /(.*)\/(edit.*|\+{2}add\+{2}.*)/;
    }

    var match_portal_type = regex_portal_type.exec(path);
    if (!(match_portal_type === null)) {
      var contenttype = match_portal_type[1];
    }

    var base_url = '';
    var match_base_url = regex_base_url.exec(path);
    if (!(match_base_url === null)) {
      base_url = match_base_url[1];
    } else {
      return;
    }

    var effective_transition = $(element).val();
    var expires_transition = $('select#form-widgets-IWFEffectiveRange-expires_transition').val();

    // get current options
    var options = $('select#form-widgets-IWFEffectiveRange-expires_transition option');
    //get expires selector
    var selector = $('select#form-widgets-IWFEffectiveRange-expires_transition');
    // remove old options
    selector.empty();

    var url = base_url + '/@@wfeffectiverange_vocab?current=' + effective_transition;

    if (typeof contenttype != 'undefined') {
      url = url + '&contenttype=' + contenttype;
    }

    $.getJSON(url, function(result) {
      //the first option is always 'no-value'
      selector.append(options[0]);

      //set new options
      $.each(result, function(idx, term) {
        var new_option = $('<option></option>');
        new_option.attr('value', term.token).text(term.token);
        selector.append(new_option);
      });
    });
  }

  var effective_element = $('select#form-widgets-IWFEffectiveRange-effective_transition');
  var expires_element = $('select#form-widgets-IWFEffectiveRange-expires_transition');

  effective_element.change(function() {
    reload_vocab(this);
  });

  if (expires_element.val() == '--NOVALUE--' && effective_element.length > 0 && effective_element.val() != '--NOVALUE--') {
    reload_vocab(effective_element);
  }

  // workaround for weird windows "last minute" change of values
  expires_element.change(function() {
    $(this).blur();
  });

});

