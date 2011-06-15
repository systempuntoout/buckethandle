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

function linkCheck() {
        link = jQuery('#link').val()
        if (jQuery('#link').text!=''){
	        jQuery('#link_check').html('&nbsp;');
	        jQuery('#link').addClass('ac_loading');
			jQuery.getJSON("/ajax/links?check="+link, function(data){
                     jQuery('#link_check').text(data.result);
                     jQuery('#link_check').addClass(data.clazz);
                     jQuery('#link').removeClass('ac_loading');
            });
     }
}

jQuery(document).ready(function() {
            jQuery(document).stacktack();
            jQuery('#post_body').markItUp(mySettings);
            jQuery("input:radio").uniform();
            linkCheck();
            jQuery("#link").typeWatch( {wait: 500,captureLength: -1, callback:linkCheck } );
});
