window.onload = function () {
    $(".basket-list").on("change", "input[type='number']", function (event) {
        var target_href = event.target;
            $.ajax({
                url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",
                success: function (data) {
                    $(".basket-list").html(data.result);
                    console.log('ajax done');
                }
            });
    });
};