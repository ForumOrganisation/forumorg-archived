$(function() {
    //Initialize Select2 Elements
    $(".select2").select2({
        language: "fr"
    });
    $("#datetime").inputmask("datetime", {
        "placeholder": "jj/mm/aaaa hh:ss"
    });
    $("#phone").intlTelInput(opt("MOBILE"));
    $("#phone_stand").intlTelInput(opt("MOBILE"));
    $("#phone_facturation").intlTelInput(opt("FIXED_LINE"));
    $("#persons").inputmask("9", {
        "placeholder": "x"
    });
    $('#banner').editable({
        mode: 'inline',
        emptytext: 'Ajoutez votre bannière',
        error: function(response, newValue) {
            if (response.status == 500) {
                return 'Impossible à modifier (section validée).';
            } else {
                return response.responseText;
            }
        }
    });
    $('.section').click(function(e) {
        e.preventDefault();
        validate_section();
        return false;
    });
});
