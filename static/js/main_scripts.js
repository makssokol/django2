'use strict';

$(document).on('click', '.details a', function(event) {
    console.log('links_menu', event)
    if (event.target.hasAttribute('href')) {
        let link = event.target.href + 'ajax/';
        let link_array = link.split('/');
        if (link_array[4] == 'category') {
            $.ajax({
                url: link,
                success: function (data) {
                    $('.details').html(data.page_content);
                },
            });
            event.preventDefault();
        }
    }
 });