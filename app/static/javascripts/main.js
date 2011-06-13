jQuery(
    function()
    {   
        jQuery("#search").focus();
        jQuery("#search, #tags").autocomplete('/ajax/tags', {
                multiple: true,
                matchContains: true,
                multipleSeparator:' '});
    }
);

jQuery(document).ready(function() {
            jQuery(document).stacktack();
            jQuery('#post_body').markItUp(mySettings);
            jQuery("input:radio").uniform();
});
