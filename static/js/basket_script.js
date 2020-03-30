jQuery(document).ready(function () {

    $('.basket-list').on('click', 'input[type="number"]', function () {
        let target_href = event.target;
        if (target_href) {
            $.ajax({
                url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",
                success: function (data) {
                    $('.basket-list').html(data.result);
                    console.log('ajax done');
                },
            });
        }
        event.preventDefault();
    });
});