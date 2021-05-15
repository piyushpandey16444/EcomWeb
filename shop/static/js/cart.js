$(document).ready(function() {
    // delete btn
    const getDeleteBtn = $(".delete__btn");
    getDeleteBtn.click(function(e) {
        e.preventDefault();
        const itemToDelete = $(this).attr("value");
        const idToDelete = {
            req_id: itemToDelete,
        };
        $.ajax({
            type: "DELETE",
            url: "/delete-item/",
            data: JSON.stringify(idToDelete),
            dataType: "json",
            success: function(response) {
                console.log("item_deleted ! ", response);
                location.reload();
            },
        });
    });

    $(".up__icon").click(function(e) {
        e.preventDefault();

        // update qty
        output = "";
        priceData = "";
        const itemId = $(this).attr("value");
        const updateField = $("#item-" + itemId);
        const mainField = $("#main-" + itemId);
        const qtyOld = updateField.attr("value");
        const qtyNew = parseInt(qtyOld) + 1;

        output +=
            "<span id='item-" +
            itemId +
            "' class='item__qty' value='" +
            qtyNew +
            "'>" +
            qtyNew +
            "</span>";
        mainField.html(output);

        // update total price
        const totalPrice = $(".total__amount-" + itemId);
        const getPrice = $("#priceof-" + itemId).attr("value");
        const newTotalPrice = parseFloat(qtyNew * getPrice).toFixed(2);
        priceData +=
            "<span id='amountof-" + itemId + "'>" + "₹ " + newTotalPrice + "</span>";
        totalPrice.html(priceData);
    });

    // qty down btn
    $(".down__icon").click(function(e) {
        e.preventDefault();
        // update qty
        output = "";
        priceData = "";
        const itemId = $(this).attr("value");
        const updateField = $("#item-" + itemId);
        const mainField = $("#main-" + itemId);
        const qtyOld = updateField.attr("value");
        if (qtyOld != 1) {
            const qtyNew = parseInt(qtyOld) - 1;
            output +=
                "<span id='item-" +
                itemId +
                "' class='item__qty' value='" +
                qtyNew +
                "'>" +
                qtyNew +
                "</span>";
            mainField.html(output);

            // update total price
            const totalPrice = $(".total__amount-" + itemId);
            const getPrice = $("#priceof-" + itemId).attr("value");
            const newTotalPrice = parseFloat(qtyNew * getPrice).toFixed(2);
            priceData +=
                "<span id='amountof-" +
                itemId +
                "'>" +
                "₹ " +
                newTotalPrice +
                "</span>";
            totalPrice.html(priceData);
        }
    });
});