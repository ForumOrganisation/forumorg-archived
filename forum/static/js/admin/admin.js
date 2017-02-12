function opt(type) {
    options = {
        autoPlaceholder: "aggressive",
        dropdownContainer: "body",
        geoIpLookup: function(callback) {
            $.get("http://ipinfo.io", function() {}, "jsonp").always(function(resp) {
                var countryCode = (resp && resp.country) ?
                    resp.country :
                    "";
                callback(countryCode);
            });
        },
        placeholderNumberType: type,
        initialCountry: "auto",
        preferredCountries: [
            'fr', 'ch', 'be', 'ma', 'nl'
        ],
        utilsScript: "{{ url_for('static', filename='js/intl_utils.js') }}"
    };
    return options;
}

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
                return 'Impossible à modifier.';
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

function validate_section() {
    var r = confirm("Pour annuler votre validation, il faudra nous contacter. Voulez-vous continuer?");
    if (r) {
        $.ajax({
            type: "POST",
            url: "{{ url_for('validate_section') }}",
            data: {
                "page": "{{ page }}"
            },
            success: function(result) {
                if (result == "success") {
                    Notify("Section validée.");
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                } else {
                    Notify("Un problème est survenu.");
                }
            }
        });
    }
}
