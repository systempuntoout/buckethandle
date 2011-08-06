jQuery(
    function()
    {   
        jQuery("#search").focus();
        jQuery("#search, #tags").autocomplete('/ajax/tags', {
                multiple: true,
                matchContains: true,
                multipleSeparator:' '});
        jQuery("#tagcloud_filter").focus();
    }
);

function linkCheck() {
        link = jQuery('#link').val()
        if (jQuery('#link').text!=''){
	        jQuery('#link_check').html('&nbsp;');
	        jQuery('#link').addClass('ac_loading');
			jQuery.getJSON("/ajax/links?check="+link, function(data){
                     jQuery('#link_check').text(data.result);
                     jQuery('#link_check').removeClass();
                     jQuery('#link_check').addClass(data.clazz);
                     jQuery('#link').removeClass('ac_loading');
            });
     }
}

function feeditemRemove(feedItemKey) {
        jQuery.ajax({
                url: '/admin/content?action=removefeeditem&key=' + feedItemKey,
                type: "POST",
                contentType: "application/x-www-form-urlencoded",
                dataType: "json",
            });
        jQuery('#'+feedItemKey).hide();
}

jQuery(document).ready(function() {
            jQuery('#content').embedly({
              maxWidth: 600,
              wmode: 'transparent',
              method: 'after'
            });
            jQuery('#post_body').markItUp(mySettings);
            jQuery("input:radio").uniform();
            jQuery("#message_box").fadeOut(6000);
            jQuery(".toggle").click(function () {
                jQuery(".totoggle").toggle();
            });
            
            setTimeout(function() {
                $('#admin_message_box').fadeOut('fast');
            }, 4000);
            if (jQuery('#link').val() && jQuery('#action').val() != 'editpost'){linkCheck();}
            jQuery("#link").typeWatch( {wait: 500,captureLength: -1, callback:linkCheck } );
            jQuery('#tagcloud_filter').keyup(function() {
                jQuery('#main_tag_cloud span.tag_info').hide().filter('span.tag_info:contains("'+this.value+'")').show();
                
            });
            
});
