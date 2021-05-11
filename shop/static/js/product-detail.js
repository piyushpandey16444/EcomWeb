$(document).ready(function() {
    $(".thumbnail").hover(function(e) {
        e.preventDefault();
        const self = this;
        $(".active").removeClass("active");
        $(".hover__on").removeClass("hover__on");
        $(self).addClass("active");
        $(self).addClass("hover__on");
        $(".product__img").attr("src", $(self).attr("src"));
    });

    // scroll btns
    const upperBtn = $(".upper__arrow");
    const lowerBtn = $(".lower__arrow");
    const sliderComponent = $(".slider");

    lowerBtn.click(function(e) {
        e.preventDefault();
        const currentPosition = $(sliderComponent).scrollTop();
        $(sliderComponent).scrollTop(currentPosition + 200);
    });

    upperBtn.click(function(e) {
        e.preventDefault();
        const currentPosition = $(sliderComponent).scrollTop();
        $(sliderComponent).scrollTop(currentPosition - 200);
    });

    // size btn selection
    const getAllSize = $(".available__size");

    getAllSize.click(function(e) {
        e.preventDefault();
        const self = $(this);
        if (self.hasClass("selected__size")) {
            self.removeClass("selected__size");
        } else {
            $(".selected__size").removeClass("selected__size");
            self.addClass("selected__size");
        }
    });

    // select color btn
    const selectedColor = $(".color");

    selectedColor.click(function(e) {
        e.preventDefault();
        const self = $(this);
        if (self.hasClass("selected__color")) {
            self.removeClass("selected__color");
        } else {
            $(".selected__color").removeClass("selected__color");
            self.addClass("selected__color");
        }
    });

    // product add to cart
    const addToCartBtnClick = $(".cart__btn");
    addToCartBtnClick.click(function(e) {
        // e.preventDefault();
        const getSelectedSize = $(".selected__size").attr("value");
        const getSelectedColor = $(".selected__color").attr("value");

        const dataToSend = {
            size: getSelectedSize,
            color: getSelectedColor,
        };

        $.ajax({
            type: "POST",
            url: "/add-to-cart/",
            data: JSON.stringify(dataToSend),
            dataType: "json",
            success: function(response) {
                console.log("response is: ", response);
            },
        });
    });
});