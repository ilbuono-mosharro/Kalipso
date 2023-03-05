$(document).ready(function () {
    $('input[type="radio"][name="ad_type"]').change(function () {
        if ($(this).val() === "SA") {
            $('#price-info').show();
        } else if ($(this).val() === "RE") {
            $('#price-info').hide();
        }
    });
});