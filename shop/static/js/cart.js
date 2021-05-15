$(document).ready(function() {
    $(".up__icon").click(function(e) {
        e.preventDefault();
        const getQty = $(this).attr("value");
        const n = $("#item-`getQty`");
        console.log(n);

        const cartData = {
            item_id: getQty,
        };
        $.ajax({
            type: "POST",
            url: "/update-qty/",
            data: JSON.stringify(cartData),
            dataType: "dataType",
            success: function(response) {
                const n = $("#item-`getQty`");
                console.log(n);
            },
        });
    });
});