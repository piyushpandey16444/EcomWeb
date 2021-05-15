$(document).ready(function() {
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
});