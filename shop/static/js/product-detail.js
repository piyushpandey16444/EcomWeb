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
        $(".selected__size").removeClass("selected__size");
        $(this).addClass("selected__size");
    });
});