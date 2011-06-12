jQuery(
    function()
    {   
        jQuery("#search").focus();
        jQuery("#search").autocomplete('/ajax/tags', {
                multiple: true,
                matchContains: true,
                multipleSeparator:' '});
    }
);

jQuery(document).ready(function() {
            jQuery(document).stacktack();
            jQuery("input:radio").uniform();
});
